from PyQt6.QtCore import QObject, pyqtSignal
from infrastructure.whisper_engine import WhisperEngine

class ModelDownloadWorker(QObject):
    """
    Loads/downloads a Whisper model in a background thread.
    
    faster-whisper downloads models automatically via Hugging Face Hub
    on first use — no manual download step needed.
    Download progress is handled internally by Hugging Face Hub
    and shown in the terminal.
    """
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int, float)  # zachowane dla kompatybilności z GUI

    def __init__(self, model: str):
        super().__init__()
        self.model = model

    def run(self):
        try:
            WhisperEngine(model_size=self.model)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))