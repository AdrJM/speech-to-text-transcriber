from dataclasses import asdict
import json
from domain.models import TranscriptionResult
from interfaces.exporter import TranscriptionExporter

class JsonExporter(TranscriptionExporter):    
    def export(self, result: TranscriptionResult, output_path: str):
        data = asdict(result)
        
        with open(output_path, "w", encoding = "utf-8") as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
    