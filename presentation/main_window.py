from pathlib import Path
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QMessageBox
)

from presentation.segment_editor_window import SegmentEditorWindow
from presentation.worker import TranscriptionWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self._thread = None
        self.last_result = None
        self.editor_window = None

        layout = QVBoxLayout()

        label = QLabel("Speech To Text")

        src_layout = QHBoxLayout()
        self.src_textbox = QLineEdit()
        src_button = QPushButton("Wybierz Plik")

        src_button.clicked.connect(self.browse_file)

        whisper_options_layout = QVBoxLayout()
        language_layout = QHBoxLayout()
        language_label = QLabel("Język ")
        self.language_combobox = QComboBox()

        self.language_combobox.addItems(["Auto", "pl", "en"])

        model_layout = QHBoxLayout()
        model_label = QLabel("Model: ")
        self.model_combobox = QComboBox()

        self.model_combobox.addItems(["tiny", "base", "small", "medium", "large"] )

        transcribe_layout = QHBoxLayout()
        self.transcribe_button = QPushButton("Transkrybuj")

        self.transcribe_button.clicked.connect(self.start_transcription)

        status_layout = QVBoxLayout()
        self.status_label = QLabel("")

        edit_layout = QVBoxLayout()
        self.edit_button = QPushButton("Edytuj")
        self.edit_button.setVisible(False)
        self.edit_button.clicked.connect(self.open_editor)


        layout.addWidget(label)
        layout.addLayout(src_layout)
        layout.addLayout(whisper_options_layout)
        layout.addLayout(transcribe_layout)
        layout.addLayout(status_layout)
        layout.addLayout(edit_layout)

        whisper_options_layout.addLayout(language_layout)
        whisper_options_layout.addLayout(model_layout)

        src_layout.addWidget(self.src_textbox)
        src_layout.addWidget(src_button)

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combobox)

        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)
        
        transcribe_layout.addWidget(self.transcribe_button)

        status_layout.addWidget(self.status_label)

        edit_layout.addWidget(self.edit_button)

        self.widget = QWidget()
        self.setCentralWidget(self.widget) 
        self.widget.setLayout(layout)
        
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik",
            filter = "Video/Audio (*.mp4 *.mkv *.avi *.wav *.mp3);;Wszystkie pliki (*)"
        )

        if path:
            self.src_textbox.setText(path)

    def start_transcription(self):
        path = self.src_textbox.text()
        language = None if self.language_combobox.currentText() == "Auto" else self.language_combobox.currentText()
        model = self.model_combobox.currentText()

        if not path:
            QMessageBox.warning(self, "Błąd", "Wybierz plik video")
            return
        
        if not Path(path).exists():
            QMessageBox.warning(self, "Błąd", f"Plik nie istnieje: {path}")
            return
        
        self.status_label.setText("Trwa transkrypcja...")

        
        
        self.worker = TranscriptionWorker(path, language, model)
        self._thread = QThread()

        self.worker.moveToThread(self._thread)
        
        self.transcribe_button.setEnabled(False)

        self._thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_transcription_finished)
        self.worker.error.connect(self.on_transcription_error)
        self.worker.finished.connect(self._thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def on_transcription_finished(self, result):
        self.last_result = result
        
        self.transcribe_button.setEnabled(True)
        self.status_label.setText("Gotowe")
        self.edit_button.setVisible(True)

    def on_transcription_error(self, message):
        self.transcribe_button.setEnabled(True)
        QMessageBox.critical(self, "Błąd", message)
    
    def open_editor(self):
        SegmentEditorWindow(self.last_result, parent = self).show()

        