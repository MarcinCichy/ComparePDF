from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# Image settings
MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB
DEFAULT_DPI = 72
DEFAULT_SENSITIVITY = 15

# UI settings
WINDOW_TITLE = 'PDF Comparator v3.0'
PREVIEW_PANEL_WIDTH = 450
PREVIEW_MIN_SIZE = (350, 150)

# Messages
MSG_LOAD_PDF_1 = "Click to load the first PDF file"
MSG_LOAD_PDF_2 = "Click to load the second PDF file"
MSG_COMPARING = "Comparing PDFs..."
MSG_SELECT_FILES = "Please upload both PDF files."
MSG_SELECT_BASE = "Please select the base file using the radio buttons."
MSG_ERROR_LOAD = "Error loading file: {}"
MSG_ERROR_COMPARE = "Error comparing documents: {}"
MSG_ERROR_GENERAL = "Wystąpił nieoczekiwany błąd: {}"

# Timeouts
PDF_LOAD_TIMEOUT = 15
COMPARISON_TIMEOUT = 30

# Colors
DIFFERENCE_COLOR = (255, 0, 0)  # Red
DIFFERENCE_OUTLINE_WIDTH = 3

# Layout
SLIDER_MIN = 1
SLIDER_MAX = 100
ZOOM_FACTOR_IN = 1.25
ZOOM_FACTOR_OUT = 0.8


def get_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette

QSS = """
    QWidget {
        font-size: 14px;
        color: #ffffff;
        background-color: #353535;
    }
    QPushButton {
        background-color: #555555;
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    QPushButton:pressed {
        background-color: #444444;
    }
    QSlider::groove:horizontal {
        border: 1px solid #444444;
        height: 8px;
        background: #555555;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #aaaaaa;
        border: 1px solid #777777;
        width: 14px;
        margin: -4px 0;
        border-radius: 7px;
    }
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
        border-radius: 7px;
        border: 1px solid #cccccc;
        background: #555555;
    }
    QRadioButton::indicator:checked {
        background-color: #00bfff;
        border: 1px solid #00bfff;
    }
    QLabel {
        font-size: 14px;
    }
"""