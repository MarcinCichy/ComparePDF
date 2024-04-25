import fitz
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QRadioButton, \
    QSpacerItem, QSizePolicy, QFileDialog, QGraphicsScene, QFrame, QButtonGroup, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
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
        self.setWindowTitle('Porównywarka PDF')
        self.mainLayout = QHBoxLayout()
        self.setupPreviewPanel()
        self.setupGraphicsView()
        self.setupSensitivityControl()  # Dodaj tę linię, aby suwak był widoczny
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

    def setupPreviewPanel(self):
        self.previewLayout = QVBoxLayout()
        self.setupFilePreview(1, "Kliknij, aby wczytać pierwszy plik PDF")
        self.setupFilePreview(2, "Kliknij, aby wczytać drugi plik PDF")
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

    def on_radio_changed(self, checked, num):
        if checked:  # Jeżeli przycisk radiowy został zaznaczony
            if self.file1 and self.file2:  # Sprawdzenie, czy oba pliki są wczytane
                self.on_compare_clicked()  # Uruchomienie porównywania
            else:
                print("Proszę wczytać oba pliki przed porównaniem.")

    def setupControlButtons(self):
        buttonsLayout = QHBoxLayout()
        for text in ["Compare", "Reset", "Clear", "Exit"]:
            btn = QPushButton(text)
            btn.clicked.connect(getattr(self, f"on_{text.lower()}_clicked"))
            buttonsLayout.addWidget(btn)
        self.previewLayout.addLayout(buttonsLayout)

    def loadFile(self, event, num):
        path, _ = QFileDialog.getOpenFileName(self, f"Wybierz plik PDF {num}", "", "PDF files (*.pdf)")
        if path:
            setattr(self, f"file{num}", path)
            self.displayPDF(path, getattr(self, f"previewLabel{num}"))

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
            print(f"Wystąpił błąd podczas próby wyświetlenia pliku PDF: {e}")

    def on_compare_clicked(self):
        if self.radio1.isChecked():
            base_file = self.file1
            compare_file = self.file2
        elif self.radio2.isChecked():
            base_file = self.file2
            compare_file = self.file1
        else:
            print("Proszę wybrać plik bazowy za pomocą przycisków radiowych.")
            return

        if base_file and compare_file:
            base_image = pdf_to_image(base_file)
            compare_image = pdf_to_image(compare_file)
            # Teraz przekazujemy również sensitivity jako argument do compare_images
            result_image = compare_images(base_image, compare_image, self.sensitivity)
            if result_image:
                q_img = pil2qimage(result_image)
                self.view.setPhoto(QPixmap.fromImage(q_img))
            else:
                print("Nie można przekonwertować obrazu.")
        else:
            print("Proszę wczytać oba pliki PDF.")

    def on_reset_clicked(self):
        self.previewLabel1.clear()
        self.previewLabel2.clear()
        self.file1, self.file2 = None, None
        self.view.setPhoto(None)  # Resetowanie widoku graficznego

    def on_clear_clicked(self):
        self.view.clearHighlights()  # Ta metoda zostanie zdefiniowana w GraphicsView

    def on_exit_clicked(self):
        self.close()
