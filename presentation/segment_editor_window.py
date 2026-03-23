
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
    QComboBox
)
from PyQt6.QtGui import QFont

from domain.models import Segment
from domain.models import TranscriptionResult
from infrastructure.export.json_exporter import JsonExporter
from infrastructure.export.srt_exporter import SrtExporter

class SegmentEditorWindow(QDialog):
    """Dialog for viewing and editing transcription segments before export."""
    def __init__(self, result, source_path: str, parent = None):
        super().__init__(parent)
        self.transcription_result = result
        self.source_path = Path(source_path)
        self.setMinimumSize(1200, 400)
        self.resize(1200, 400)
        self.segment_rows = []

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

        self.format_combobox = QComboBox()
        self.format_combobox.addItems(["JSON", "SRT"])

        self.srt_mode_combobox = QComboBox()
        self.srt_mode_combobox.addItems(["Per wyraz", "Per segment"])
        self.srt_mode_combobox.setVisible(False)

        self.format_combobox.currentTextChanged.connect(self._on_format_changed)

        button = QPushButton("Eksportuj")
        button.clicked.connect(self._export)

        layout.addLayout(label_layout)
        layout.addWidget(scroll)
        layout.addLayout(button_layout)

        label_layout.addWidget(label)
        button_layout.addWidget(self.format_combobox)
        button_layout.addWidget(self.srt_mode_combobox)
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
        self.segment_rows.append((start_field, text_field, end_field))
    
    def _export(self):
        fmt = self.format_combobox.currentText()

        if fmt == "JSON":
            self._export_json()
        else:
            self._export_srt()

    def _get_current_result(self) -> TranscriptionResult:
        """Reads current values from editor fields and returns updated TranscriptionResult."""
        segments = []
        for i, (start_field, text_field, end_field) in enumerate(self.segment_rows):
            segments.append(Segment(
                id=i,
                start=float(start_field.text()),
                end=float(end_field.text()),
                text=text_field.text()
            ))
        return TranscriptionResult(
            language=self.transcription_result.language,
            segments=segments
        )

    def _export_json(self):
        """Exports transcription result to JSON file next to the source file."""
        output_path = self.source_path.with_suffix(".json")
        JsonExporter().export(self._get_current_result(), output_path)
        QMessageBox.information(self, "Eksport", f"Zapisano do {output_path.name}")

    def _export_srt(self):
        """ Exports transcription result to SRT file next to the source file."""
        output_path = self.source_path.with_suffix(".srt")
        word_level = self.srt_mode_combobox.currentText() == "Per wyraz"
        SrtExporter().export(self._get_current_result(), output_path, word_level = word_level)
        QMessageBox.information(self, "Eksport", f"Zapisano do {output_path.name}")

    def _on_format_changed(self, fmt: str):
        self.srt_mode_combobox.setVisible(fmt == "SRT")