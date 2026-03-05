from dataclasses import dataclass
from typing import List

@dataclass
class Segment:
    id: int
    start: float
    end: float
    text: str

@dataclass
class TranscriptionResult:
    language: str
    segments: List[Segment]