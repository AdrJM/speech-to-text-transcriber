import subprocess
from pathlib import Path

class AudioExtractor:
    def extract(self, video_path: str, output_path: str) -> str:
        video = Path(video_path)
        output = Path(output_path)

        command = [
            "ffmpeg",
            "-i", str(video),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output)
        ]

        subprocess.run(command, check=True)

        return str(output)