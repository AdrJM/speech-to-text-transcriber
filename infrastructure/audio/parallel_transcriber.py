import torch
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from interfaces.engines import TranscriptionEngine
from domain.models import Segment, TranscriptionResult
from domain.mappers import map_to_domain

class ParallelTranscriber:
    """
    On CPU: uses multiple threads — safe because Whisper releases the GIL during inference.
    On GPU (CUDA): parallel threads still work but share the same GPU, so gains are smaller.
        For true GPU parallelism you would need multiple GPUs and separate model instances.

    Usage:
        transcriber = ParallelTranscriber(engine, max_workers=4)
        result = transcriber.transcribe_chunks(chunks, language="pl")
    """

    def __init__(self, engine: TranscriptionEngine, max_workers: int | None = None):
        self.engine = engine 

        # Automatically detect device and pick a sensible default for max_workers.
        # On GPU: default to 2 (GPU memory is the bottleneck, not CPU cores).
        # On CPU: default tp 4
        if max_workers is not None:
            self.max_workers = max_workers
        elif torch.cuda.is_available():
            self.max_workers = 2
        else:
            self.max_workers = 4

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def transcribe_chunks(self, chunks: list[tuple[Path, float]], language: str = "pl") -> tuple[list[Segment], str]:
        """
        Transcribes a list of (chunk_path, offset) tuples in parallel.
        Returns (segments, detected_language) — same shape as TranscriptionService._transcribe_chunks.
        """
        
        results: dict[int, tuple[list[Segment], str]] = {}

        with ThreadPoolExecutor(max_workers = self.max_workers) as executor:
            #Submit all chunks, keeping track of their index so we can
            # reassemble them in order after parallel execution.
            future_to_index = {
                executor.submit(self._transcribe_single, chunk_path, offset, language): i
                for i, (chunk_path, offset) in enumerate(chunks)
            }

            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    segments, detected_language = future.result()
                    results[index] = (segments, detected_language)
                except Exception as e:
                    raise RuntimeError(f"Chunk {index} failed during transcription: {e}") from e
                
        # Reassemble in original order
        all_segments = []
        detected_language = None

        for i in sorted(results):
            segments, lang = results[i]
            if detected_language is None:
                detected_language = lang
            all_segments.extend(segments)

        return all_segments, detected_language or language
    
    def _transcribe_single(self, chunk_path: Path, offset: float, language: str) -> tuple[list[Segment], str]:
        """Transcribes one chunk and applies the time offset to all segments."""
        raw_result = self.engine.transcribe(chunk_path, language)
        result = map_to_domain(raw_result)

        for segment in result.segments:
            segment.start += offset
            segment.end += offset

        return result.segments, result.language
    