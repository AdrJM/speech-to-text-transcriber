LIGHT = {
    "bg": "#ffffff",
    "text": "#000000",
    "border": "#000000",
    "button_bg": "#000000",
    "button_text": "#ffffff",
    "input_bg": "#ffffff",
    "input_border": "#000000",
    "disabled": "#888888",
}

DARK = {
    "bg": "#0a0a0a",
    "text": "#ffffff",
    "border": "#ffffff",
    "button_bg": "#ffffff",
    "button_text": "#000000",
    "input_bg": "#1a1a1a",
    "input_border": "#ffffff",
    "disabled": "#555555",
}
def build_title_bar_button_style(colors: dict) -> str:
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {colors['text']};
            border: none;
            font-size: 20px;
            font-family: 'Courier New', monospace;
        }}
        QPushButton:hover {{
            background-color: {colors['border']};
            color: {colors['bg']};
        }}
    """

def build_stylesheet(colors: dict) -> str:
    return f"""
        QMainWindow, QWidget, QDialog {{
            background-color: {colors['bg']};
            color: {colors['text']};
            font-family: 'Courier New', monospace;
        }}
        QPushButton {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
            border: 2px solid {colors['border']};
            border-radius: 0px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }}
        QPushButton:hover {{
            background-color: {colors['bg']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
        }}
        QPushButton:disabled {{
            background-color: {colors['disabled']};
            color: {colors['bg']};
            border: 2px solid {colors['disabled']};
        }}
        QLineEdit {{
            background-color: {colors['input_bg']};
            color: {colors['text']};
            border: 2px solid {colors['input_border']};
            border-radius: 0px;
            padding: 4px 8px;
            font-size: 13px;
            font-family: 'Courier New', monospace;
        }}
        QComboBox {{
            background-color: {colors['input_bg']};
            color: {colors['text']};
            border: 2px solid {colors['input_border']};
            border-radius: 0px;
            padding: 4px 8px;
            font-size: 13px;
            font-family: 'Courier New', monospace;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox::item:hover {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
        }}
        QComboBox::item:selected {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
        }}
        QComboBox QAbstractItemView {{
            background-color: {colors['input_bg']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            selection-background-color: {colors['button_bg']};
            selection-color: {colors['button_text']};
        }}
        QCheckBox {{
            color: {colors['text']};
            font-size: 13px;
            font-family: 'Courier New', monospace;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {colors['border']};
            border-radius: 0px;
            background-color: {colors['bg']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors['button_bg']};
        }}
        QLabel {{
            color: {colors['text']};
            font-size: 13px;
            font-family: 'Courier New', monospace;
        }}
        QScrollArea {{
            border: 2px solid {colors['border']};
        }}
        QScrollBar:vertical {{
            background-color: {colors['bg']};
            width: 12px;
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            min-height: 20px;
        }}
    """