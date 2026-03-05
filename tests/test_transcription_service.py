import pytest
from application.transcription_service import TranscriptionService

class DummyEngine:
    def transcribe(self, audio_path, language):
        return "test transcription"
    
def test_transcription_service_returns_text():
    service = TranscriptionService(DummyEngine())
    result = service.transcribe_file("fake.wav")

    assert result == "test transcription"