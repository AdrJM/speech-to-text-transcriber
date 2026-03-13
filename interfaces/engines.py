from typing import Any, Protocol
from pathlib import Path

class TranscriptionEngine(Protocol):
    model_size: str
    
    def transcribe(self, audio_path: Path, language: str) -> Any:
        ...