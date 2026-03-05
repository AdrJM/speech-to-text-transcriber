import os
import argparse
import sys
from infrastructure.whisper_engine import WhisperEngine
from application.transcription_service import TranscriptionService
from infrastructure.export.json_exporter import JsonExporter
from config.settings import MODEL_SIZE

def main():
    parser = argparse.ArgumentParser(description = "Speech to Text Application")
    parser.add_argument("audio_path", help = "Path to audio file")
    parser.add_argument("--language", default = "pl", help = "Language code")

    args = parser.parse_args()

    if not os.path.exists(args.audio_path):
        print("File does not exist")
        sys.exit(1)

    engine = WhisperEngine(model_size = MODEL_SIZE)
    service = TranscriptionService(engine)
    exporter = JsonExporter()
    
    result = service.transcribe_file(args.audio_path)
    print("\n--- TRANSCRIPTION ---\n")
    exporter.export(result, "output.json")


if __name__ == "__main__":
    main()