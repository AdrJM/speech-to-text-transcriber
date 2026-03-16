
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QWidget,
    QLineEdit,
    QMessageBox,
)
from PyQt6.QtGui import QFont

from domain.models import TranscriptionResult
from infrastructure.export.json_exporter import JsonExporter

class SegmentEditorWindow(QDialog):
    """Dialog for viewing and editing transcription segments before export."""
    def __init__(self, result, source_path: str, parent = None):
        super().__init__(parent)
        self.transcription_result = result
        self.source_path = Path(source_path)
        self.setMinimumSize(1200, 400)
        self.resize(1200, 400)

        layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        label = QLabel("Transkrybcja")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)

        for segment in result.segments:
            self._add_segment_row(segment, container_layout)

        scroll.setWidget(container)

        button = QPushButton("Eksportuj")
        button.clicked.connect(self._export)

        layout.addLayout(label_layout)
        layout.addWidget(scroll)
        layout.addLayout(button_layout)

        label_layout.addWidget(label)
        button_layout.addWidget(button)

        self.setLayout(layout)

    def _add_segment_row(self, segment, container_layout):
        """Adds a single editable row (start, text, end) for a segment."""
        font = QFont()
        font.setPointSize(11)

        row = QHBoxLayout()
    
        start_field = QLineEdit(str(segment.start))
        text_field = QLineEdit(segment.text)
        end_field = QLineEdit(str(segment.end))
    
        start_field.setFont(font)
        text_field.setFont(font)
        end_field.setFont(font)

        start_field.setFixedHeight(30)
        start_field.setFixedWidth(60)
        text_field.setFixedHeight(30)
        end_field.setFixedHeight(30)
        end_field.setFixedWidth(60)

        row.addWidget(start_field)
        row.addWidget(text_field)
        row.addWidget(end_field)
    
        container_layout.addLayout(row)
    
    def _export(self):
        """Exports transcription result to JSON file next to the source file."""
        output_path = self.source_path.with_suffix(".json")
        JsonExporter().export(self.transcription_result, output_path)
        QMessageBox.information(self, "Eksport", f"Zapisano do {output_path.name}")