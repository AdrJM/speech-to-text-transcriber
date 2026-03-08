from abc import ABC, abstractmethod
from domain.models import TranscriptionResult
from pathlib import Path

class TranscriptionExporter(ABC):

    @abstractmethod
    def export(self, result: TranscriptionResult, output_path: Path):
        pass
    