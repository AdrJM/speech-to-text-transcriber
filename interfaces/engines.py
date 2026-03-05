from typing import Protocol

class TranscriptionEngine(Protocol):
    def transcribe(self, audio_path: str, language: str) -> str:
        return "Transcribe"