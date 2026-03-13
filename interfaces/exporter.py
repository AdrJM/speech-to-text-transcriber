from abc import ABC, abstractmethod
from domain.models import TranscriptionResult
from pathlib import Path

class TranscriptionExporter(ABC):
    """Abstract base class for transcription exporters."""

    @abstractmethod
    def export(self, result: TranscriptionResult, output_path: Path):
        """Exports transcription result to the given output path."""
        pass
    