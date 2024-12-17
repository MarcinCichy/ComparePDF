from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
                             QRadioButton, QSpacerItem, QSizePolicy, QGraphicsScene, QFrame,
                             QSlider, QMessageBox, QFileDialog, QProgressDialog)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from graphics_view import GraphicsView
from utils import PDFComparator

class PDFComparatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Comparator v2.0")
        self.setGeometry(100, 100, 1200, 800)
        self.pdf_comparator = PDFComparator()

        # Pliki PDF
        self.file1 = None
        self.file2 = None

        # Główne elementy GUI
        self.init_ui()
        self.progress_dialog = None

    def init_ui(self):
        # Layout główny
        self.main_layout = QHBoxLayout()

        # Panel boczny
        self.side_panel = QVBoxLayout()
        self.setup_file_preview("Load the first PDF file", 1)
        self.setup_file_preview("Load the second PDF file", 2)
        self.setup_controls()
        self.setup_sensitivity_slider()

        # Widok wynikowy
        self.graphics_scene = QGraphicsScene()
        self.graphics_view = GraphicsView(self.graphics_scene)
        self.main_layout.addWidget(self.graphics_view)

        # Centralny widget
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_layout.addLayout(self.side_panel)
        central_layout.addLayout(self.main_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def setup_file_preview(self, text, file_num):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumSize(300, 200)
        label.mousePressEvent = lambda event, num=file_num: self.load_file(event, num)
        setattr(self, f"file_preview_{file_num}", label)
        self.side_panel.addWidget(label)

    def setup_controls(self):
        controls_layout = QHBoxLayout()
        compare_btn = QPushButton("Compare")
        compare_btn.clicked.connect(self.on_compare_clicked)
        controls_layout.addWidget(compare_btn)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.on_reset_clicked)
        controls_layout.addWidget(reset_btn)

        self.side_panel.addLayout(controls_layout)

    def setup_sensitivity_slider(self):
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Sensitivity of recognize differences:")
        slider_layout.addWidget(slider_label)

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(100)
        self.sensitivity_slider.setValue(15)
        self.sensitivity_slider.valueChanged.connect(self.update_sensitivity)
        slider_layout.addWidget(self.sensitivity_slider)

        self.side_panel.addLayout(slider_layout)

    def load_file(self, event, file_num):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a PDF file", "", "PDF Files (*.pdf)")
        if file_path:
            setattr(self, f"file{file_num}", file_path)
            label = getattr(self, f"file_preview_{file_num}")
            label.setText(f"Loaded: {file_path}")
            pixmap = self.pdf_comparator.pdf_to_image(file_path)
            if pixmap:
                label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def update_sensitivity(self):
        self.pdf_comparator.sensitivity = self.sensitivity_slider.value()

    def on_compare_clicked(self):
        if not self.file1 or not self.file2:
            QMessageBox.warning(self, "Error", "Please load both PDF files before comparing.")
            return

        self.progress_dialog = QProgressDialog("Comparing PDFs...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()

        result_image, _ = self.pdf_comparator.compare_pdfs(self.file1, self.file2)
        self.progress_dialog.close()

        if result_image:
            pixmap = QPixmap.fromImage(result_image)
            self.graphics_view.setPhoto(pixmap)
        else:
            QMessageBox.warning(self, "Error", "Failed to compare the PDF files.")

    def on_reset_clicked(self):
        self.file1 = None
        self.file2 = None
        self.file_preview_1.setText("Load the first PDF file")
        self.file_preview_2.setText("Load the second PDF file")
        self.graphics_view.setPhoto(None)
