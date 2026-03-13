from dataclasses import dataclass
from typing import List

@dataclass
class Segment:
    """Represents a single transcribed segment with timing information."""
    id: int
    start: float    # start time in seconds
    end: float      # end time in seconds
    text: str

@dataclass
class TranscriptionResult:
    """Represents the full transcription result containing all segments and detected language."""
    language: str
    segments: List[Segment]