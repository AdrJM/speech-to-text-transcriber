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
    QMessageBox,
    QCheckBox
)

from presentation.workers.model_download_worker import ModelDownloadWorker
from presentation.segment_editor_window import SegmentEditorWindow
from presentation.workers.transcription_worker import TranscriptionWorker

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

        checkbox_layout = QVBoxLayout()
        self.split_checkbox = QCheckBox("Podziel audio na chunki")
        self.split_checkbox.stateChanged.connect(self._on_split_toggled)
        self.parallel_checkbox = QCheckBox("Transkrybuj równolegle")
        self.parallel_checkbox.setEnabled(False)

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
        layout.addLayout(checkbox_layout)

        whisper_options_layout.addLayout(language_layout)
        whisper_options_layout.addLayout(model_layout)

        src_layout.addWidget(self.src_textbox)
        src_layout.addWidget(src_button)

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combobox)

        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)

        checkbox_layout.addWidget(self.split_checkbox)
        checkbox_layout.addWidget(self.parallel_checkbox)

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

        if not self._is_model_downloaded(model):
            reply = QMessageBox.question(
                self, 
                "Brak modelu",
                f"Model '{model}' nie jest pobrany. Pobrać go teraz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            self._start_download_model(model)
            return
        
        output = Path(path).parent / "audio" / Path(path).with_suffix(".wav").name

        if output.exists():
            reply = QMessageBox.question(
                self, "Plik istnieje",
                f"Plik '{output.name}' już istnieje. Nadpisać?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.status_label.setText("Trwa transkrypcja...")

        
        
        self.worker = TranscriptionWorker(path, language, model, self.split_checkbox.isChecked(), self.parallel_checkbox.isChecked())
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

    def _is_model_downloaded(self, model: str) -> bool:
        possible_dirs = [
            Path.home() / ".cache" / "whisper",
            Path.home() / ".var" / "app" / "com.visualstudio.code" / "cache" / "whisper",
        ]
        for cache_dir in possible_dirs:
            print(f"Sprawdzam: {cache_dir}, istnieje: {cache_dir.exists()}")
            if cache_dir.exists():
                files = list(cache_dir.glob(f"{model}*"))
                print(f"Znalezione pliki: {files}")
                if files:
                    return True
        return False
    # def _is_model_downloaded(self, model: str) -> bool:
    #     possible_dirs = [
    #         Path.home() / ".cache" / "whisper",
    #         Path.home() / ".var" / "app" / "com.visualstudio.code" / "cache" / "whisper",
    #     ]
    #     for cache_dir in possible_dirs:
    #         if cache_dir.exists() and list(cache_dir.glob(f"{model}*")):
    #             return True
    #     return False
    
    def _start_download_model(self, model: str):
        self.transcribe_button.setEnabled(False)
        self.status_label.setText(f"Pobieranie modelu '{model}'...")

        self.download_worker =  ModelDownloadWorker(model)
        self._thread_for_download = QThread()

        self.download_worker.moveToThread(self._thread_for_download)

        self._thread_for_download.started.connect(self.download_worker.run)
        self.download_worker.progress.connect(self._on_download_progress)
        self.download_worker.finished.connect(self._on_model_downloaded)
        self.download_worker.error.connect(self.on_transcription_error)
        self.download_worker.finished.connect(self._thread_for_download.quit)
        self.download_worker.finished.connect(self.download_worker.deleteLater)
        self._thread_for_download.finished.connect(self._thread_for_download.deleteLater)

        self._thread_for_download.start()

    def _on_model_downloaded(self):
        self.transcribe_button.setEnabled(True)
        self.status_label.setText("Model pobrany. Możesz transkrybować.")
    
    def _on_download_progress(self, percent: int, speed: float):
        speed_mb = speed / 1024 / 1024
        self.status_label.setText(f"Pobieranie modelu... {percent}% ({speed_mb:.1f} MB/s)")

    def _on_split_toggled(self, state):
        self.parallel_checkbox.setEnabled(state == 2)
        if state != 2:
            self.parallel_checkbox.setChecked(False)