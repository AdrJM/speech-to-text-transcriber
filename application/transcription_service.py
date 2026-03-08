from interfaces.engines import TranscriptionEngine
from domain.mappers import map_to_domain
from domain.models import TranscriptionResult
from pathlib import Path

class TranscriptionService:
    def __init__(self, engine: TranscriptionEngine, audio_splitter = None, audio_extractor = None, parallel_transcriber = None):
        self.engine = engine
        self.audio_splitter = audio_splitter
        self.audio_extractor = audio_extractor
        self.parallel_transcriber = parallel_transcriber

    def transcribe_file(self, file_path: Path, language: str = "pl") -> TranscriptionResult:
        file_path = Path(file_path)

        if not file_path:
            raise ValueError("File path cannot be empty")
        
        if not file_path.exists():
            raise FileNotFoundError(file_path)
        
        audio_path = self._prepare_audio(file_path)
        chunks = self._get_chunks(audio_path)
        segments, detected_language = self._transcribe_chunks(chunks, language)
        segments = self._reindex_segments(segments)

        return TranscriptionResult(
            language = detected_language,
            segments = segments
            )
        
    def _prepare_audio(self, file_path: Path) -> Path:
        if self.audio_extractor and file_path.suffix != ".wav":
            return self.audio_extractor.extract(file_path)
        
        return file_path

    def _get_chunks(self, audio_path: Path):
        if self.audio_splitter:
            return self.audio_splitter.split(audio_path)
    
        return [(audio_path, 0)]
    
    def _transcribe_chunks(self, chunks, language):
        if self.parallel_transcriber:
            return self.parallel_transcriber.transcribe_chunks(chunks, language)
        
        all_segments = []
        detected_language = None
        
        for chunk_path, offset in chunks:
            raw_result = self.engine.transcribe(chunk_path, language)
            result = map_to_domain(raw_result)

            if detected_language is None:
                detected_language = result.language
            
            for segment in result.segments:
                segment.start += offset
                segment.end += offset
            
            all_segments.extend(result.segments)
        
        return all_segments, detected_language or language

    def _reindex_segments(self, segments):
        for i, segment in enumerate(segments):
            segment.id = i
        return segments
