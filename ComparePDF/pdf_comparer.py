import fitz
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QRadioButton, \
    QSpacerItem, QSizePolicy, QFileDialog, QGraphicsScene, QFrame, QButtonGroup, QSlider, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter
from utils import pil2qimage, pdf_to_image, compare_images
from graphics_view import GraphicsView


class PDFComparer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sensitivity = 15  # Ustawienie domyślnej wartości czułości
        self.mainLayout = None
        self.centralWidget = None
        self.previewLayout = None
        self.radioGroup = QButtonGroup()  # Grupa dla przycisków radiowych
        self.previewLabel1 = None
        self.previewLabel2 = None
        self.radio1 = None
        self.radio2 = None
        self.file1 = None
        self.file2 = None
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('PDF Comparator')
        self.mainLayout = QHBoxLayout()
        self.setupPreviewPanel()
        self.setupGraphicsView()
        self.setupSensitivityControl()  # Dodaj tę linię, aby suwak był widoczny
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

    def setupPreviewPanel(self):
        self.previewLayout = QVBoxLayout()
        self.setupFilePreview(1, "Click to load the first PDF file")
        self.setupFilePreview(2, "Click to load the second PDF file")
        self.setupControlButtons()
        previewWidget = QWidget()
        previewWidget.setLayout(self.previewLayout)
        previewWidget.setMaximumWidth(450)
        self.mainLayout.addWidget(previewWidget)

    def setupSensitivityControl(self):
        self.sensitivityLabel = QLabel("Sensitivity of recognize differences:")
        self.sensitivityValueLabel = QLabel("{:03d}".format(15))  # Początkowa wartość z suwaka

        self.sensitivitySlider = QSlider(Qt.Horizontal)
        self.sensitivitySlider.setMinimum(1)
        self.sensitivitySlider.setMaximum(100)
        self.sensitivitySlider.setValue(15)  # Ustawienie domyślnej wartości czułości
        self.sensitivitySlider.valueChanged.connect(self.updateSensitivity)

        # Ustawienie polityki rozmiaru i minimalnych/maksymalnych wymiarów
        self.sensitivitySlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sensitivitySlider.setMinimumWidth(200)  # Minimalna szerokość suwaka
        self.sensitivitySlider.setMaximumWidth(205)  # Maksymalna szerokość suwak

        layout = QHBoxLayout()  # Tworzenie nowego layoutu do trzymania etykiety i suwaka
        layout.addWidget(self.sensitivityLabel)
        layout.addWidget(self.sensitivitySlider)
        layout.addWidget(self.sensitivityValueLabel)  # Etykieta wartości jest tuż obok suwaka

        # Dodanie elastycznego miejsca na końcu, aby wyrównać suwak do lewej
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        self.previewLayout.addLayout(layout)  # Dodanie layoutu do głównego panelu

    def updateSensitivity(self, value):
        self.sensitivity = value
        self.sensitivityValueLabel.setText("{:03d}".format(value))

    def setupGraphicsView(self):
        scene = QGraphicsScene()
        self.view = GraphicsView(scene)
        self.mainLayout.addWidget(self.view)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setupFilePreview(self, num, text):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumSize(350, 150)
        label.mousePressEvent = lambda event, num=num: self.loadFile(event, num)
        radio = QRadioButton()
        self.radioGroup.addButton(radio, num)  # Dodanie przycisku do grupy z identyfikatorem num
        radio.toggled.connect(lambda checked, num=num: self.on_radio_changed(checked, num))  # Dodanie sygnału toggled
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(radio)
        widget = QWidget()
        widget.setLayout(layout)
        self.previewLayout.addWidget(widget)
        setattr(self, f"previewLabel{num}", label)
        setattr(self, f"radio{num}", radio)
        if num == 1:
            radio.setChecked(True)

    def setupControlButtons(self):
        buttonsLayout = QHBoxLayout()
        for text in ["Compare", "Reset", "Clear", "Print"]:
            btn = QPushButton(text)
            btn.clicked.connect(getattr(self, f"on_{text.lower()}_clicked"))
            buttonsLayout.addWidget(btn)
        self.previewLayout.addLayout(buttonsLayout)

    def loadFile(self, event, num):
        try:
            path, _ = QFileDialog.getOpenFileName(self, f"Select a PDF file {num}", "", "PDF files (*.pdf)")
            if path:
                setattr(self, f"file{num}", path)
                self.displayPDF(path, getattr(self, f"previewLabel{num}"))
        except Exception as e:
            print(f"An error occurred while loading the PDF file: {e}")
            QMessageBox.critical(self, "Loading error", f"An error occurred while loading the PDF file: {e}")

    def displayPDF(self, path, label):
        try:
            doc = fitz.open(path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
            doc.close()
        except Exception as e:
            print(f"An error occurred while trying to view the PDF file: {e}")
            QMessageBox.critical(self, "Display error", f"Error displaying PDF: {e}")

    def on_compare_clicked(self):
        if self.radio1.isChecked():
            base_file = self.file1
            compare_file = self.file2
        elif self.radio2.isChecked():
            base_file = self.file2
            compare_file = self.file1
        else:
            print("Please select the base file using the radio buttons.")
            return

        if base_file and compare_file:
            base_image = pdf_to_image(base_file)
            compare_image = pdf_to_image(compare_file)
            result_image, original_image = compare_images(base_image, compare_image, self.sensitivity)
            if result_image and original_image:
                self.result_image = pil2qimage(result_image)  # Obraz z czerwonymi ramkami
                self.original_image = pil2qimage(original_image)  # Czysty obraz bazowy
                self.view.setPhoto(QPixmap.fromImage(self.result_image))  # Domyślnie pokazuje wynik
            else:
                print("The image could not be converted.")
        else:
            print("Please upload both PDF files.")

    def on_reset_clicked(self):
        if self.previewLabel1 and self.previewLabel2:
            self.previewLabel1.clear()  # Czyści wyświetlanie obrazów
            self.previewLabel2.clear()
        self.file1, self.file2 = None, None  # Resetuje zmienne plików
        if self.view:
            self.view.setPhoto(None)  # Czyści wyświetlany obraz w GraphicsView

    def on_clear_clicked(self):
        if hasattr(self, 'original_image'):  # Sprawdzenie, czy oryginalny obraz jest dostępny
            self.view.setPhoto(QPixmap.fromImage(self.original_image))  # Ustawienie czystego obrazu bazowego
            print("The view has been reset to the original base image.")
        else:
            print("No base image available")

    def on_print_clicked(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            # Drukowanie zawartości GraphicsView
            self.view.render(painter)
            painter.end()

    def on_radio_changed(self, checked, num):
        if checked:  # Jeżeli przycisk radiowy został zaznaczony
            if self.file1 and self.file2:  # Sprawdzenie, czy oba pliki są wczytane
                self.on_compare_clicked()  # Uruchomienie porównywania
            else:
                print("Please load both files before comparing.")

