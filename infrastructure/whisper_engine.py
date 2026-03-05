import whisper
import torch

class WhisperEngine:
    def __init__(self, model_size: str = "medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_size = model_size
        self.model = self._load_model()

    def _load_model(self):
        print(f"Loading Whisper model '{self.model_size}' on '{self.device}'...")
        return whisper.load_model(self.model_size, device=self.device)
    
    def transcribe(self, audio_path: str, language:str = "pl") -> dict:
        result = self.model.transcribe(
            audio_path,
            language = language,
            fp16 = torch.cuda.is_available()
        )
        
        return result