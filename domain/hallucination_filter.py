import re

_PATTERNS = [
    r"napisy\s+(i\s+lektor\s+)?by\s+jacek\s+makarewicz",
    r"subtitles?\s+by\s+\w+",
    r"napisy\s+dla\s+niesłyszących",
    r"amara\.org",
    r"thank\s+you\s+for\s+watching",
    r"please\s+(like\s+and\s+)?subscribe",
    r"transcribed\s+by",
    r"captioned\s+by",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _PATTERNS]

def is_hallucination(text: str) -> bool:
    if not text.strip():
        return True
    return any(p.search(text) for p in _COMPILED)