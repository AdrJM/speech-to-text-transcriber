import pytest
from domain.models import TranscriptionResult
from domain.mappers import map_to_domain


def test_map_to_domain_returns_transcription_result():
    raw = {"language": "pl", "segments": []}
    result = map_to_domain(raw)
    assert isinstance(result, TranscriptionResult)

def test_map_to_domain_maps_segments():
    raw = {
        "language": "pl",
        "segments": [
            {"id": 0, "start": 0.0, "end": 2.0, "text": "hello"}
        ]
    }
    result = map_to_domain(raw)
    assert len(result.segments) == 1
    assert result.segments[0].text == "hello"

def test_map_to_domain_maps_words():
    raw = {
        "language": "pl",
        "segments": [
            {
                "id": 0, "start": 0.0, "end": 2.0, "text": "hello world",
                "words": [
                    {"word": "hello", "start": 0.0, "end": 1.0},
                    {"word": "world", "start": 1.0, "end": 2.0}
                ]
            }
        ]
    }
    result = map_to_domain(raw)
    assert len(result.segments[0].words) == 2
    assert result.segments[0].words[0].word == "hello"

def test_map_to_domain_raises_on_invalid_language():
    raw = {"language": 123, "segments": []}
    with pytest.raises(ValueError):
        map_to_domain(raw)

