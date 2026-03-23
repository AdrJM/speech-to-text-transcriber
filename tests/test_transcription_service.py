from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from application.transcription_service import TranscriptionService
from domain.models import TranscriptionResult

class DummyEngine:
    model_size = "tiny"
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
        model_size = "tiny"
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
    mock_splitter.chunk_length_sec = 60
    mock_splitter.split_single.side_effect = [
        [(chunk1, 0)],
        [(chunk2, 60)]
    ]
    with patch("application.transcription_service.subprocess.run") as mock_run:
        mock_run.return_value.stdout = "120\n"  # 2 minuty = 2 chunki po 60s
        service = TranscriptionService(DummyEngineWithSegment(), mock_splitter)
        transcribe = service.transcribe_file(audio, "pl")
    
    assert transcribe.segments[1].start == 60.0