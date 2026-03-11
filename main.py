
import argparse
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from presentation.main_window import MainWindow
from infrastructure.whisper_engine import WhisperEngine
from application.transcription_service import TranscriptionService
from infrastructure.export.json_exporter import JsonExporter
from config.settings import MODEL_SIZE

#   CLI
def main():
    parser = argparse.ArgumentParser(description = "Speech to Text Application")
    parser.add_argument("audio_path", help = "Path to audio file")
    parser.add_argument("--language", default = "pl", help = "Language code")

    args = parser.parse_args()

    audio_path = Path(args.audio_path)

    if not audio_path.exists():
        print(f"Error: File '{audio_path}' does not exist.")
        sys.exit(1)
    
    try:
        engine = WhisperEngine(model_size = MODEL_SIZE)
        service = TranscriptionService(engine)
        exporter = JsonExporter()

        result = service.transcribe_file(audio_path, args.language)

        output_file = audio_path.with_suffix(".json")
        exporter.export(result, output_file)

        print(f"\nTranscription saved to {output_file}")
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

#   GUI
def run_gui():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()     # CLI
    else:
        run_gui()  # GUI