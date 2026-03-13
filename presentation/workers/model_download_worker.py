from PyQt6.QtCore import QObject, pyqtSignal
from tqdm import tqdm
import whisper

class TqdmSignal(tqdm):
    def __init__(self, *args, signal = None, **kwargs):
        self.signal = signal
        super().__init__(*args, **kwargs)

    def update(self, n = 1):
        super().update(n)
        if self.signal and self.total:
            percent = int(self.n / self.total * 100)
            speed = self.format_dict.get("rate", 0) or 0
            self.signal.emit(percent, speed)

class ModelDownloadWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int, float)

    def __init__(self, model: str):
        super().__init__()
        self.model = model

    def run(self):
        try:
            original_tqdm = getattr(whisper, "tqdm")
            setattr(whisper, "tqdm", lambda *a, **kw: TqdmSignal(*a, signal = self.progress, **kw))

            whisper.load_model(self.model)

            setattr(whisper, "tqdm", original_tqdm)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))