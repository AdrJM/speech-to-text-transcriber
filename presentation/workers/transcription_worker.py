from pathlib import Path
from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

from application.transcription_service import TranscriptionService
from infrastructure.audio.audio_extractor import AudioExtractor
from infrastructure.audio.audio_splitter import AudioSplitter
from infrastructure.audio.parallel_transcriber import ParallelTranscriber
from infrastructure.whisper_engine import WhisperEngine

class TranscriptionWorker(QObject):
    def __init__(self, audio_path, language, model, use_split, use_parallel):
        super().__init__()
        self.use_split = use_split
        self.use_parallel = use_parallel
        self.audio_path = audio_path
        self.language = language
        self.model = model

    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def run(self):
        try:
            engine = WhisperEngine(model_size = self.model)
            extractor = AudioExtractor()
            splitter = AudioSplitter()
            parallel = ParallelTranscriber(engine)
            service = TranscriptionService(
                engine, 
                audio_extractor = extractor,
                audio_splitter = splitter if self.use_split else None,
                parallel_transcriber = parallel if self.use_parallel else None
                )
            
            results = service.transcribe_file(Path(self.audio_path), self.language)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))