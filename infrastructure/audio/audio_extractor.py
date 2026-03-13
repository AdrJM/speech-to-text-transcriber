import subprocess
from pathlib import Path

class AudioExtractor:
    
    """
    Extracts audio from video files using ffmpeg.
    
    Converts video to a 16kHz mono WAV file optimized for Whisper transcription.
    Output is saved to an 'audio/' subdirectory next to the source file.
    """
    
    def extract(self, video_path: Path) -> Path:
        """
        Extracts audio track from video_path and saves it as a WAV file.
        Returns the path to the extracted WAV file.
        """
        
        video = Path(video_path)
        output = video_path.parent / "audio" / video_path.with_suffix(".wav").name
        output.parent.mkdir(parents=True, exist_ok=True)

        command = [
            "ffmpeg",
            "-y",
            "-i", str(video),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output)
        ]

        subprocess.run(command, check=True)

        return output