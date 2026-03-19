from domain.models import TranscriptionResult
from interfaces.exporter import TranscriptionExporter
from pathlib import Path

class SrtExporter(TranscriptionExporter):
    """Exports transcription results to SRT subtitle format."""

    MAX_LINE_LENGTH = 16

    def export(self, result: TranscriptionResult, output_path: Path, word_level: bool = True):
        """Serializes TranscriptionResult to SRT and writes it to output_path"""

        subtitle_index = 1
        
        with open(output_path, "w", encoding="utf-8") as f:
            for segment in result.segments:
                if word_level and segment.words:
                    groups = self._group_words(segment.words)
                    for group in groups:
                        start = group[0].start
                        end = group[-1].end
                        text = " ".join(w.word for w in group)
                        f.write(f"{subtitle_index}\n")
                        f.write(f"{self._format_time(start)} --> {self._format_time(end)}\n")
                        f.write(f"{text}\n\n")
                        subtitle_index += 1
                else:
                    f.write(f"{segment.id + 1}\n")
                    f.write(f"{self._format_time(segment.start)} --> {self._format_time(segment.end)}\n")
                    f.write(f"{segment.text}\n\n")

    def _group_words(self, words):
        """Groups words into lines not exceeding MAX_LINE_LENGTH characters."""
    
        groups = []
        current_group = []
        current_length = 0

        for word in words:
            word_len = len(word.word) + (1 if current_group else 0) # +1 for space
            if current_group and current_length + word_len > self.MAX_LINE_LENGTH:
                groups.append(current_group)
                current_group = [word]
                current_length = len(word.word)
            else:
                current_group.append(word)
                current_length += word_len

        if current_group:
            groups.append(current_group)

        return groups

    def _format_time(self, seconds: float) -> str:
        """Converts seconds to SRT time format HH:MM:SS, mmm."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"