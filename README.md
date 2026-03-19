# Speech-to-Text Transcriber

> **Work in progress** — the project is under active development. Some features may be incomplete or change without notice.

Whisper-based speech-to-text transcription tool with a PyQt6 GUI and structured JSON output.

---

## Features

- Transcription powered by [OpenAI Whisper](https://github.com/openai/whisper)
- PyQt6 GUI with real-time status updates
- Video support — extracts audio from MP4, MKV, AVI automatically via ffmpeg
- Audio splitting — splits long files into chunks to reduce memory usage
- Parallel transcription — transcribes chunks simultaneously using multiple threads
- Download progress — shows % and MB/s when downloading Whisper models
- Transcription progress — shows how many chunks have been processed
- Segment editor — view and edit transcribed segments before export
- JSON export — saves transcription with timestamps to a structured JSON file
- SRT export — exports subtitles with word-level or segment-level timestamps
- CLI mode — run transcription directly from the terminal

---

## Requirements

- Python 3.11+
- ffmpeg installed and available in PATH

---

## Installation

```bash
git clone https://github.com/AdrJM/speech-to-text-transcriber.git
cd speech-to-text-transcriber

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## Usage

### GUI
```bash
python main.py
```

### CLI
```bash
python main.py path/to/audio.wav --language pl
```

---

## Configuration

Create a `.env` file in the project root:

```env
MODEL_SIZE=medium
LANGUAGE=pl
```

---

## Project Structure

```
application/        # transcription service (business logic)
config/             # settings and environment variables
domain/             # data models and mappers
infrastructure/     # Whisper engine, audio extractor, splitter, parallel transcriber, JSON/SRT exporter
interfaces/         # protocols (TranscriptionEngine, TranscriptionExporter)
presentation/       # PyQt6 GUI (main window, segment editor, workers)
tests/              # pytest tests
main.py             # CLI and GUI entry point
```

---

## Supported Models

| Model  | Size   | Speed   | Accuracy |
|--------|--------|---------|----------|
| tiny   | 75 MB  | fastest | lowest   |
| base   | 142 MB | fast    | low      |
| small  | 466 MB | medium  | medium   |
| medium | 1.5 GB | slow    | high     |
| large  | 3 GB   | slowest | highest  |

Models are downloaded automatically on first use.

---

## Roadmap

- [ ] Highlight detection - automatically find the most interesting moments in the video
- [ ] DaVinci Resolve plugin — auto-montage shorts/tiktoks based on highlights (separate project)
- [ ] AMD GPU support (ROCm)
- [ ] Add more language options to GUI
- [ ] Save edited segments from editor back to result
- [ ] Transcription progress for non-chunked files

---

## License

MIT