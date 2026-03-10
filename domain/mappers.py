from domain.models import Segment, TranscriptionResult


def map_to_domain(result: dict) -> TranscriptionResult:
        segments = []

        for segment in result.get("segments", []):
            segments.append(
                Segment(
                    id = segment.get("id"),
                    start = segment.get("start"),
                    end = segment.get("end"),
                    text = segment.get("text", "").strip()
                )
            )

        language = result.get("language")

        if not isinstance(language, str):
            raise ValueError("Invalid language returned from Whisper")
        
        return TranscriptionResult(
            language = language, 
            segments = segments
        )