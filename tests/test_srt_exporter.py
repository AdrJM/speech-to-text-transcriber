import pytest
from domain.models import Segment, TranscriptionResult, Word
from domain.mappers import map_to_domain
from infrastructure.export.srt_exporter import SrtExporter


@pytest.fixture
def simple_result():
    return TranscriptionResult(
        language="pl",
        segments=[
            Segment(id=0, start=0.0, end=2.5, text="Hello world", words=[]),
            Segment(id=1, start=2.5, end=5.0, text="Goodbye world", words=[]),
        ]
    )

@pytest.fixture
def result_with_words():
    return TranscriptionResult(
        language="pl",
        segments=[
            Segment(
                id=0, start=0.0, end=4.0, text="Hello world",
                words=[
                    Word(word="Hello", start=0.0, end=2.0),
                    Word(word="world", start=2.0, end=4.0),
                ]
            )
        ]
    )

def test_srt_exporter_creates_file(tmp_path, simple_result):
    output = tmp_path / "output.srt"
    SrtExporter().export(simple_result, output)
    assert output.exists()

def test_srt_exporter_per_segment(tmp_path, simple_result):
    output = tmp_path / "output.srt"
    SrtExporter().export(simple_result, output, word_level=False)
    content = output.read_text()
    assert "Hello world" in content
    assert "Goodbye world" in content

def test_srt_exporter_format(tmp_path, simple_result):
    output = tmp_path / "output.srt"
    SrtExporter().export(simple_result, output, word_level=False)
    content = output.read_text()
    assert "00:00:00,000 --> 00:00:02,500" in content

def test_srt_exporter_word_level(tmp_path, result_with_words):
    output = tmp_path / "output.srt"
    SrtExporter().export(result_with_words, output, word_level=True)
    content = output.read_text()
    assert "Hello" in content
    assert "world" in content

def test_srt_exporter_fallback_to_segment_when_no_words(tmp_path, simple_result):
    output = tmp_path / "output.srt"
    SrtExporter().export(simple_result, output, word_level=True)
    content = output.read_text()
    assert "Hello world" in content