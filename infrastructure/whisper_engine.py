from faster_whisper import WhisperModel 
from pathlib import Path

class WhisperEngine:
    """
    Wraps faster-whisper model for audio transcription.
    
    Runs on CPU with int8 quantization to minimize memory usage
    and avoid conflicts with GPU-heavy applications like DaVinci Resolve.
    Future: add device parameter for CUDA/ROCm support.
    """
    def __init__(self, model_size: str = "medium"):
        self.device = "cpu"
        self.compute_type = "int8"
        self.model_size = model_size
        self.model = self._load_model()

    def _load_model(self):
        """Loads Whisper model onto the selected device."""        
        return WhisperModel(
            self.model_size,
            device = self.device,
            compute_type = self.compute_type
        )
    
    def transcribe(self, audio_path: Path, language: str = "pl") -> dict:
        """
        Transcribes audio file and returns dict compatible with existing map_to_domain.
        Converts faster-whisper segment objects to openai-whisper-style dict format.
        """
        segments_generator, info = self.model.transcribe(
            str(audio_path),
            language = language,
            word_timestamps = True
        )

        segments = []

        for i, segment in enumerate(segments_generator):
            words = [
                {
                    "word": w.word,
                    "start": w.start,
                    "end": w.end
                }
                for w in (segment.words or [])
            ]
            segments.append({
                "id": i,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": words
            })
        
        return {
            "segments": segments,
            "language": info.language
        }