from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QWidget,
    QLineEdit
)

class SegmentEditorWindow(QDialog):
    def __init__(self, result, parent = None):
        super().__init__(parent)

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

        layout.addLayout(label_layout)
        layout.addLayout(button_layout)
        layout.addWidget(scroll)

        label_layout.addWidget(label)
        button_layout.addWidget(button)

        self.setLayout(layout)

    def _add_segment_row(self, segment, container_layout):
        row = QHBoxLayout()
    
        start_field = QLineEdit(str(segment.start))
        text_field = QLineEdit(segment.text)
        end_field = QLineEdit(str(segment.end))
    
        row.addWidget(start_field)
        row.addWidget(text_field)
        row.addWidget(end_field)
    
        container_layout.addLayout(row)
    