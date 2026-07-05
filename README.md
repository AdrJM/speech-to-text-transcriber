# Speech-to-Text Transcriber

Whisper-based speech-to-text transcription tool with a PyQt6 GUI and structured JSON/SRT output.

---

## Features

- Transcription powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2 backend)
- Custom PyQt6 GUI with dark/light theme toggle
- Video support — extracts audio from MP4, MKV, AVI automatically via ffmpeg
- Audio splitting — splits long files into chunks to reduce memory usage
- Parallel transcription — multiple threads on CPU
- Transcription progress — shows how many chunks have been processed
- Segment editor — view and edit transcribed segments before export
- JSON export — saves transcription with timestamps
- SRT export — word-level or segment-level subtitles
- CLI mode — run transcription directly from the terminal

---

## Requirements

- Python 3.12
- ffmpeg installed and available in PATH

---

## Installation

```bash
git clone https://github.com/AdrJM/speech-to-text-transcriber.git
cd speech-to-text-transcriber

python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Hugging Face Token (recommended)

Whisper models are downloaded automatically from Hugging Face Hub on first use.
Without a token, downloads still work but with lower rate limits.

To get a token:
1. Create a free account at [huggingface.co](https://huggingface.co)
2. Go to **Settings → Access Tokens → New Token**
3. Select type `read` and enable **Read access to contents of all public gated repos you can access**
4. Copy the token and add it to your `.env` file:

```env
HF_TOKEN=hf_your_token_here
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
infrastructure/     # Whisper engine, audio extractor, splitter, parallel transcriber, exporters
interfaces/         # protocols (TranscriptionEngine, TranscriptionExporter)
presentation/       # PyQt6 GUI (main window, segment editor, workers, style)
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

Models are downloaded automatically on first use via Hugging Face Hub.

---

## GPU Support

Currently the engine runs on CPU with `int8` quantization via CTranslate2, which significantly reduces memory usage compared to the previous PyTorch-based implementation — making it safe to run alongside GPU-heavy applications like DaVinci Resolve.

GPU acceleration is planned for a future release:

- [ ] **NVIDIA (CUDA)** — faster-whisper natively supports CUDA; planned as the next GPU backend
- [ ] **AMD (ROCm)** — requires building CTranslate2 with HIP support from source; planned after CUDA support is stable

---

## Roadmap

- [ ] NVIDIA GPU support (CUDA) via faster-whisper
- [ ] AMD GPU support (ROCm) via CTranslate2-HIP
- [ ] DaVinci Resolve integration — import generated SRT directly into timeline via Lua script
- [ ] Highlight detection — automatically find the most interesting moments in the video
- [ ] DaVinci Resolve plugin — auto-montage shorts/TikToks based on highlights (separate project)
- [ ] Add more language options to GUI
- [ ] Transcription progress for non-chunked files

---

## License

MIT