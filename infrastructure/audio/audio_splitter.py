import subprocess
from pathlib import Path

class AudioSplitter:
    
    """
    Splits audio files into fixed-length chunks using ffmpeg.
    
    Uses ffmpeg instead of pydub to avoid loading the entire file into RAM,
    which would cause memory issues with large files.
    """
    
    def split(self, file_path: Path, chunk_length_sec: int = 60):

        """
        Splits audio into chunks of chunk_length_sec seconds.
        Returns a list of (chunk_path, offset) tuples where offset is the
        start time of the chunk in seconds relative to the original file.
        Chunks smaller than 1KB are skipped (empty or corrupted).
        """

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
            if chunk_path.stat().st_size > 1000:  # skip empty/corrupted chunks
                chunks.append((chunk_path, offset))
            
            offset += chunk_length_sec
            index += 1
            
        return chunks