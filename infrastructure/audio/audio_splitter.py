import subprocess
from pydub import AudioSegment
from pathlib import Path

class AudioSplitter:
    def split(self, file_path: Path, chunk_length_sec: int = 60):
        output_path = Path(file_path).parent / "chunks"
        output_path.mkdir(parents = True, exist_ok = True)

        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
            capture_output=True, text=True, check=True
        )
        duration = float(result.stdout.strip())

        chunks = []
        index = 0
        offset = 0

        while offset < duration:
            chunk_path = output_path / f"chunk_{index}.wav"

            subprocess.run([
                "ffmpeg", "-y",
                "-i", str(file_path),
                "-ss", str(offset),
                "-t", str(chunk_length_sec),
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                str(chunk_path)
            ], check = True)
            if chunk_path.stat().st_size > 1000:  # > 1KB
                chunks.append((chunk_path, offset))
            
            offset += chunk_length_sec
            index += 1
            
        return chunks