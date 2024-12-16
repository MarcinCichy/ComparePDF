from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QRadioButton, QButtonGroup)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from config.settings import MSG_LOAD_PDF_1, MSG_LOAD_PDF_2

class PreviewPanel(QWidget):
    file_clicked = pyqtSignal(int)
    base_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.radio_group = QButtonGroup()

        container1 = QHBoxLayout()
        container_widget1 = QWidget()
        self.pdf1_area = ClickableLabel(MSG_LOAD_PDF_1)
        self.radio1 = QRadioButton()
        self.radio1.setChecked(True)
        self.radio_group.addButton(self.radio1, 1)
        container1.addWidget(self.pdf1_area)
        container1.addWidget(self.radio1)
        container_widget1.setLayout(container1)

        container2 = QHBoxLayout()
        container_widget2 = QWidget()
        self.pdf2_area = ClickableLabel(MSG_LOAD_PDF_2)
        self.radio2 = QRadioButton()
        self.radio_group.addButton(self.radio2, 2)
        container2.addWidget(self.pdf2_area)
        container2.addWidget(self.radio2)
        container_widget2.setLayout(container2)

        self.layout.addWidget(container_widget1)
        self.layout.addWidget(container_widget2)

    def _connect_signals(self):
        self.pdf1_area.clicked.connect(lambda: self.file_clicked.emit(1))
        self.pdf2_area.clicked.connect(lambda: self.file_clicked.emit(2))
        self.radio_group.buttonClicked[int].connect(self.base_changed.emit)

    def update_preview(self, doc_num: int, pixmap: QPixmap):
        if doc_num == 1:
            self.pdf1_area.setPixmap(pixmap)
        else:
            self.pdf2_area.setPixmap(pixmap)

    def clear_preview(self, doc_num: int):
        if doc_num == 1:
            self.pdf1_area.clear()
            self.pdf1_area.setText(MSG_LOAD_PDF_1)
        else:
            self.pdf2_area.clear()
            self.pdf2_area.setText(MSG_LOAD_PDF_2)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(200, 150)
        self.setStyleSheet("border: 1px solid gray;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
