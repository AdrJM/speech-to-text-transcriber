from dataclasses import dataclass, field
from typing import List

@dataclass
class Word:
    """Represents a single transcribed word with timing information."""
    word: str
    start: float
    end: float
    
@dataclass
class Segment:
    """Represents a single transcribed segment with timing information."""
    id: int
    start: float    # start time in seconds
    end: float      # end time in seconds
    text: str
    words: List[Word] = field(default_factory = list)

@dataclass
class TranscriptionResult:
    """Represents the full transcription result containing all segments and detected language."""
    language: str
    segments: List[Segment]