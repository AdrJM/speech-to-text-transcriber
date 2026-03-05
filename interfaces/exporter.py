from abc import ABC, abstractmethod
from domain.models import TranscriptionResult

class TranscriptionExporter(ABC):

    @abstractmethod
    def export(self, result: TranscriptionResult, output_path: str):
        pass
    