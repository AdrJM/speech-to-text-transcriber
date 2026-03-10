from pathlib import Path
from unittest.mock import MagicMock
import pytest
from application.transcription_service import TranscriptionService
from domain.models import TranscriptionResult

class DummyEngine:
    def transcribe(self, audio_path, language):
        return {
            "language": language,
            "segments": []
        }
@pytest.fixture
def service():
    service = TranscriptionService(DummyEngine())
    return service

@pytest.fixture
def audio(tmp_path):
    audio = tmp_path / "test.wav"
    audio.write_bytes(b"fake")

    return audio 

def test_transcription_service_returns_transcription_result(service, audio):
    transcribe = service.transcribe_file(audio, "pl")

    assert isinstance(transcribe, TranscriptionResult)

def test_segment_id_is_reindexed(service, audio):
    transcribe = service.transcribe_file(audio, "pl")
    i=0

    for segment in transcribe.segments:
        assert segment.id == i
        i += 1

def test_chunks_offset(tmp_path):
    class DummyEngineWithSegment:
        def transcribe(self, audio_path, language):
            return {
                "language": language,
                "segments": [
                    {"id": 0, "start": 0.0, "end": 2.0, "text": "hello"}
                ]
            }
    
    audio = tmp_path / "test.wav"
    chunk1 = tmp_path / "chunk_0.wav"
    chunk2 = tmp_path / "chunk_1.wav"

    audio.write_bytes(b"fake")
    chunk1.write_bytes(b"fake")
    chunk2.write_bytes(b"fake")

    mock_splitter = MagicMock()
    mock_splitter.split.return_value = [(chunk1, 0), (chunk2, 60)]
    
    service = TranscriptionService(DummyEngineWithSegment(), mock_splitter)
    transcribe = service.transcribe_file(audio, "pl")
    
    assert transcribe.segments[1].start == 60.0