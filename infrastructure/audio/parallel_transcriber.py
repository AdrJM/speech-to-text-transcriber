import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from interfaces.engines import TranscriptionEngine
from infrastructure.whisper_engine import WhisperEngine
from domain.models import Segment
from domain.mappers import map_to_domain

class ParallelTranscriber:
    """
    Transcribes audio chunks in parallel using a thread pool.

    Each thread gets its own Whisper model instance (via threading.local)
    to avoid sharing state between threads.
    Chunks are processed in batches of max_workers to limit memory usage.

    On CPU: uses multiple threads — safe because faster-whisper releases
    the GIL during inference.

    Future: when GPU support is added, default max_workers should drop to 1
    since GPU handles parallelism internally.

    Usage:
        transcriber = ParallelTranscriber(engine, max_workers=4)
        result = transcriber.transcribe_chunks(chunks, language="pl")
    """

    def __init__(self, engine: TranscriptionEngine, max_workers: int | None = None):
        self.engine = engine
        self._local = threading.local()
        self.max_workers = max_workers if max_workers is not None else 4

    def _init_worker(self):
        """Called once per thread when executor starts."""
        self._local.engine = WhisperEngine(model_size=self.engine.model_size)

    def transcribe_chunks(self, chunks: list[tuple[Path, float]], language: str = "pl", on_progress=None) -> tuple[list[Segment], str]:
        """
        Transcribes a list of (chunk_path, offset) tuples in parallel.
        Returns (segments, detected_language).
        """
        results: dict[int, tuple[list[Segment], str]] = {}
        future_to_index: dict = {}
        batch_size = self.max_workers

        with ThreadPoolExecutor(
            max_workers=self.max_workers,
            initializer=self._init_worker
        ) as executor:
            for batch_start in range(0, len(chunks), batch_size):
                batch = chunks[batch_start:batch_start + batch_size]
                future_to_index = {
                    executor.submit(self._transcribe_single, chunk_path, offset, language): batch_start + i
                    for i, (chunk_path, offset) in enumerate(batch)
                }
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        results[index] = future.result()
                        if on_progress:
                            on_progress(len(results), len(chunks))
                    except Exception as e:
                        raise RuntimeError(f"Chunk {index} failed: {e}") from e

        all_segments = []
        detected_language = None

        for i in sorted(results):
            segments, lang = results[i]
            if detected_language is None:
                detected_language = lang
            all_segments.extend(segments)

        return all_segments, detected_language or language

    def _get_engine(self):
        """Returns the engine instance for the current thread, creating it if needed."""
        if not hasattr(self._local, "engine"):
            self._local.engine = WhisperEngine(model_size=self.engine.model_size)
        return self._local.engine

    def _transcribe_single(self, chunk_path: Path, offset: float, language: str) -> tuple[list[Segment], str]:
        """Transcribes one chunk and applies the time offset to all segments."""
        engine = self._get_engine()
        raw_result = engine.transcribe(chunk_path, language)
        result = map_to_domain(raw_result)

        for segment in result.segments:
            segment.start += offset
            segment.end += offset

        return result.segments, result.language