from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from presentation.style import LIGHT, build_title_bar_button_style, DARK

class TitleBarMixin:
    """Mixin providing custom title bar and window dragging functionality."""
    
    def init_title_bar(self):
        self._drag_pos = QPoint()
        self._title_bar_btns = []  # ← dodaj

    def apply_frameless(self, dialog: bool = False):
        flags = Qt.WindowType.FramelessWindowHint
        if dialog:
            flags |= Qt.WindowType.Dialog
        self.setWindowFlags(flags) # type: ignore

    def build_title_bar(self, title: str, show_max: bool = True, on_theme_toggle = None, theme = None) -> QWidget:
        colors = theme or DARK
        title_bar = QWidget()
        title_bar.setFixedHeight(46)
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(0)

        if on_theme_toggle:
            btn_theme = QPushButton("☀")
            btn_theme.setFixedSize(50, 46)
            btn_theme.setStyleSheet(build_title_bar_button_style(colors) + "QPushButton { font-size: 14px; }")
            btn_theme.clicked.connect(on_theme_toggle)
            self._title_bar_btns.append(btn_theme)
                
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")

        btn_close = QPushButton("✕")
        btn_min = QPushButton("—")

        buttons = [btn_close, btn_min]

        if show_max:
            btn_max = QPushButton("▢")
            btn_max.setFixedSize(46, 46)
            btn_max.setStyleSheet(build_title_bar_button_style(colors) + "QPushButton { font-size: 14px; }")
            btn_max.clicked.connect(lambda: self.showNormal() if self.isMaximized() else self.showMaximized()) # type: ignore
            buttons.append(btn_max)
            self._title_bar_btns.append(btn_max)

        for btn in [btn_min, btn_close]:
            btn.setFixedSize(46, 46)
            btn.setStyleSheet(build_title_bar_button_style(colors))
            self._title_bar_btns.append(btn)

        btn_min.clicked.connect(self.showMinimized) # type: ignore
        btn_close.clicked.connect(self.close) # type: ignore

        layout.addWidget(title_label)
        layout.addStretch()
        
        if on_theme_toggle:
            layout.addWidget(btn_theme)

        layout.addWidget(btn_min)
        if show_max:
            layout.addWidget(btn_max)
        layout.addWidget(btn_close)

        return title_bar

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft() # type: ignore

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos) # type: ignore
    