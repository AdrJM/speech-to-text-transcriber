from typing import Any, Protocol
from pathlib import Path

class TranscriptionEngine(Protocol):
    def transcribe(self, audio_path: Path, language: str) -> Any:
        ...