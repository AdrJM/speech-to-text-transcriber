import subprocess
from pathlib import Path

class AudioExtractor:
    def extract(self, video_path: Path) -> Path:
        video = Path(video_path)
        output = video_path.parent / "audio" / video_path.with_suffix(".wav").name
        output.parent.mkdir(parents=True, exist_ok=True)

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

        return output