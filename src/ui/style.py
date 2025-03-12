"""
UI Stylesheet for the Universal File Converter
"""

STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

QLabel {
    font-size: 11pt;
}

QGroupBox {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    margin-top: 1em;
    font-size: 11pt;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QPushButton {
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 10pt;
}

QPushButton:hover {
    background-color: #2a75f3;
}

QPushButton:pressed {
    background-color: #1e65d9;
}

QPushButton:disabled {
    background-color: #bdbdbd;
    color: #f5f5f5;
}

QComboBox {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    padding: 5px 10px;
    min-width: 6em;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: #bdbdbd;
    border-left-style: solid;
}

QLineEdit {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    padding: 5px;
}

QListWidget {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
}

QProgressBar {
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #4285f4;
    width: 10px;
    margin: 0px;
}

QCheckBox {
    font-size: 10pt;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}
"""