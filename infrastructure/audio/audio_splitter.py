from pydub import AudioSegment
from pathlib import Path

class AudioSplitter:
    def split(self, audio_path: Path, output_path: Path, chunk_length_sec: int = 60):
        audio = AudioSegment.from_wav(audio_path)

        chunk_length_ms = chunk_length_sec * 1000
        output_path.mkdir(parents = True, exist_ok = True)

        chunks = []

        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]

            index = i // chunk_length_ms
            offset = index * chunk_length_sec
            
            output = output_path / f"chunk_{index}.wav"
            
            chunk.export(output, format="wav")
            chunks.append((output, offset))

        return chunks