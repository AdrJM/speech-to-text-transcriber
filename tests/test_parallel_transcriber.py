from pathlib import Path

import pytest
from domain.models import Segment
from infrastructure.audio.parallel_transcriber import ParallelTranscriber


class DummyEngine:
    def transcribe(self, audio_path, language):
        return {
            "language": language,
            "segments": []
        }

class DummyEngineWithSegment:
        def transcribe(self, audio_path, language):
            return {
                "language": language,
                "segments": [
                    {"id": 0, "start": 0.0, "end": 2.0, "text": "chunk1"},
                    ]
            }
        

@pytest.fixture
def create_chunks(tmp_path):
    chunk1 = tmp_path / "chunk_0.wav"
    chunk2 = tmp_path / "chunk_1.wav"
    chunk1.write_bytes(b"fake")
    chunk2.write_bytes(b"fake")

    return chunk1, chunk2

def test_transcribe_chunks_returns_correct_type(create_chunks):
    chunk1, chunk2 = create_chunks
    chunks = [(chunk1, 0.0), (chunk2, 60.0)]
    parallel = ParallelTranscriber(DummyEngine(), max_workers = 2)
    result = parallel.transcribe_chunks(chunks)

    segments, language = result
    assert isinstance(segments, list)
    assert isinstance(language, str)

def test_transcribe_chunks_returns_segments_in_correct_order_with_offset(create_chunks):
    chunk1, chunk2 = create_chunks
    chunks = [(chunk1, 0.0), (chunk2, 60.0)]
    parallel = ParallelTranscriber(DummyEngineWithSegment(), max_workers = 2)
    segments, language = parallel.transcribe_chunks(chunks)

    assert segments[0].start == 0.0    
    assert segments[1].start == 60.0

def test_transcribe_chunks_raises_on_engine_error(create_chunks):
    class DummyEngineThatFails:
        def transcribe(self, audio_path, language):
            raise ValueError("Transcription failed")
        
    chunk1, chunk2 = create_chunks
    chunks = [(chunk1, 0.0), (chunk2, 60.0)]
    parallel = ParallelTranscriber(DummyEngineThatFails(), max_workers = 2)
    
    with pytest.raises(RuntimeError):
        parallel.transcribe_chunks(chunks)
