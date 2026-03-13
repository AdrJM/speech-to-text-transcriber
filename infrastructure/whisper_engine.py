import whisper
import torch
from pathlib import Path

class WhisperEngine:
    """
    Wraps OpenAI Whisper model for audio transcription.
    
    Automatically selects CUDA if available, otherwise falls back to CPU.
    Model is loaded once in __init__ to avoid reloading on every transcription.
    """
    def __init__(self, model_size: str = "medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_size = model_size
        self.model = self._load_model()

    def _load_model(self):
        """Loads Whisper model onto the selected device."""        
        return whisper.load_model(self.model_size, device=self.device)
    
    def transcribe(self, audio_path: Path, language: str = "pl") -> dict:
        """Transcribes audio file and returns raw Whisper output dict."""
        results = self.model.transcribe(
            str(audio_path),
            language = language,
            fp16 = torch.cuda.is_available()
        )
        
        return results