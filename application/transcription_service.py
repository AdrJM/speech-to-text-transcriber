from ..interfaces.engines import TranscriptionEngine
from ..domain.models import Segment
from ..domain.models import TranscriptionResult

class TranscriptionService:
    def __init__(self, engine: TranscriptionEngine):
        self.engine = engine

    def transcribe_file(self, file_path: str, language: str = "pl") -> TranscriptionResult:
        if not file_path:
            raise ValueError("File path cannot be empty")
        
        raw_result = self.engine.transcribe(file_path, language)
        return self._map_to_domain(raw_result)
    
    def _map_to_domain(self, result: dict) -> TranscriptionResult:
        segments = []

        for segment in result.get("segments", []):
            segments.append(
                Segment(
                    id = segment.get("id"),
                    start = segment.get("start"),
                    end = segment.get("end"),
                    text = segment.get("text", "").strip()
                )
            )

        language = result.get("language")

        if not isinstance(language, str):
            raise ValueError("Invalid language returned from Whisper")
        
        return TranscriptionResult(
            language = language,
            segments = segments
        )
    
        
    