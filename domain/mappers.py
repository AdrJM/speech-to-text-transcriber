from domain.models import Segment, TranscriptionResult, Word


def map_to_domain(result: dict) -> TranscriptionResult:
        """
        Maps raw Whisper output dict to domain objects.
        
        Raises ValueError if language is missing or not a string.
        """
        segments = []

        for segment in result.get("segments", []):
            words = [
                 Word(
                      word = w.get("word", "").strip(),
                      start = w.get("start", 0.0),
                      end = w.get("end", 0.0)
                 )
                 for w in segment.get("words", [])
            ]

            segments.append(
                Segment(
                    id = segment.get("id"),
                    start = segment.get("start"),
                    end = segment.get("end"),
                    text = segment.get("text", "").strip(),
                    words = words
                )
            )

        language = result.get("language")

        if not isinstance(language, str):
            raise ValueError("Invalid language returned from Whisper")
        
        return TranscriptionResult(
            language = language, 
            segments = segments
        )