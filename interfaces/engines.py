from typing import Any, Protocol
from pathlib import Path

class TranscriptionEngine(Protocol):
    """Protocol defining the interface for transcription engines."""
    model_size: str
    
    def transcribe(self, audio_path: Path, language: str) -> Any:
        """Transcribes audio file and returns raw engine output."""
        ...