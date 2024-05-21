import fitz
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QRadioButton, \
    QSpacerItem, QSizePolicy, QFileDialog, QGraphicsScene, QFrame, QButtonGroup, QSlider, QMessageBox
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot, QMetaObject, Q_ARG, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap, QImage, QPainter
from utils import pil2qimage, pdf_to_image, compare_images
from graphics_view import GraphicsView

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB, zmień wartość w razie potrzeby

class PDFLoadTask(QRunnable):
    def __init__(self, callback, file_path, num, parent):
        super().__init__()
        self.callback = callback
        self.file_path = file_path
        self.num = num
        self.parent = parent

    def run(self):
        try:
            print(f"Loading PDF file: {self.file_path}")
            doc = fitz.open(self.file_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            QMetaObject.invokeMethod(self.parent, "loadFinished", Qt.QueuedConnection, Q_ARG(QPixmap, pixmap), Q_ARG(int, self.num))
        except Exception as e:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection, Q_ARG(str, f"Failed to load or process PDF file: {e}"))
        finally:
            doc.close()

class PDFComparer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sensitivity = 15
        self.mainLayout = None
        self.centralWidget = None
        self.previewLayout = None
        self.radioGroup = QButtonGroup()
        self.previewLabel1 = None
        self.previewLabel2 = None
        self.radio1 = None
        self.radio2 = None
        self.file1 = None
        self.file2 = None
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('PDF Comparator v1.5')
        self.mainLayout = QHBoxLayout()
        self.setupPreviewPanel()
        self.setupGraphicsView()
        self.setupSensitivityControl()
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
        self.sensitivityValueLabel = QLabel("{:03d}".format(15))
        self.sensitivitySlider = QSlider(Qt.Horizontal)
        self.sensitivitySlider.setMinimum(1)
        self.sensitivitySlider.setMaximum(100)
        self.sensitivitySlider.setValue(15)
        self.sensitivitySlider.valueChanged.connect(self.updateSensitivity)
        self.sensitivitySlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sensitivitySlider.setMinimumWidth(200)
        self.sensitivitySlider.setMaximumWidth(205)
        layout = QHBoxLayout()
        layout.addWidget(self.sensitivityLabel)
        layout.addWidget(self.sensitivitySlider)
        layout.addWidget(self.sensitivityValueLabel)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        self.previewLayout.addLayout(layout)

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
        self.radioGroup.addButton(radio, num)
        radio.toggled.connect(lambda checked, num=num: self.on_radio_changed(checked, num))
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
                task = PDFLoadTask(self.loadFinished, path, num, self)
                QThreadPool.globalInstance().start(task)
        except Exception as e:
            self.showError(f"Failed to load PDF file: {str(e)}")

    @pyqtSlot(QPixmap, int)
    def loadFinished(self, pixmap, num):
        label = getattr(self, f"previewLabel{num}")
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    @pyqtSlot(str)
    def showError(self, message):
        QMessageBox.critical(self, "Error", message)

    def on_compare_clicked(self):
        try:
            if self.file1 and self.file2:
                if self.radio1.isChecked():
                    base_file = self.file1
                    compare_file = self.file2
                elif self.radio2.isChecked():
                    base_file = self.file2
                    compare_file = self.file1
                else:
                    QMessageBox.warning(self, "Selection Error", "Please select the base file using the radio buttons.")
                    return
                task = ImageCompareTask(base_file, compare_file, self.sensitivity, self.compareFinished, self)
                QThreadPool.globalInstance().start(task)
            else:
                QMessageBox.warning(self, "File Error", "Please upload both PDF files.")
        except Exception as e:
            error_msg = f"An error occurred: {e}."
            self.showError(error_msg)

    @pyqtSlot(object, object)
    def compareFinished(self, result_image, original_image):
        try:
            if result_image and original_image:
                print("Successfully compared images.")
                self.result_image = pil2qimage(result_image)
                self.original_image = pil2qimage(original_image)

                # Sprawdź rozmiar wynikowego obrazu
                buffer = QByteArray()
                buffer_device = QBuffer(buffer)
                buffer_device.open(QIODevice.WriteOnly)
                self.result_image.save(buffer_device, "PNG")
                buffer_device.close()
                image_size = buffer.size()

                if image_size > MAX_IMAGE_SIZE:
                    self.showError(
                        f"Resulting image is too large to display ({image_size / (1024 * 1024):.2f} MB). Please reduce the sensitivity or try smaller PDFs.")
                    return

                print(f"Result image size: {self.result_image.size()}")
                print(f"Original image size: {self.original_image.size()}")

                pixmap = QPixmap.fromImage(self.result_image)
                print("Setting photo in GraphicsView.")
                self.view.setPhoto(pixmap)
                print("Photo set successfully in GraphicsView.")
            else:
                self.showError("Failed to generate comparison results.")
        except Exception as e:
            self.showError(f"Error displaying comparison results: {e}")
            print(f"Exception: {e}")

    def on_reset_clicked(self):
        if self.previewLabel1 and self.previewLabel2:
            self.previewLabel1.clear()
            self.previewLabel2.clear()
        self.file1, self.file2 = None, None
        if self.view:
            self.view.setPhoto(None)

    def on_clear_clicked(self):
        if hasattr(self, 'original_image'):
            self.view.setPhoto(QPixmap.fromImage(self.original_image))

    def on_print_clicked(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            self.view.render(painter)
            painter.end()

    def on_radio_changed(self, checked, num):
        if checked:
            if self.file1 and self.file2:
                self.on_compare_clicked()


class ImageCompareTask(QRunnable):
    def __init__(self, base_file, compare_file, sensitivity, callback, parent):
        super().__init__()
        self.base_file = base_file
        self.compare_file = compare_file
        self.sensitivity = sensitivity
        self.callback = callback
        self.parent = parent

    def run(self):
        try:
            print(f"Comparing images: {self.base_file} vs {self.compare_file}")
            base_image = pdf_to_image(self.base_file)
            if base_image is None:
                raise ValueError(f"Failed to convert {self.base_file} to image.")
            compare_image = pdf_to_image(self.compare_file)
            if compare_image is None:
                raise ValueError(f"Failed to convert {self.compare_file} to image.")
            result_image, original_image = compare_images(base_image, compare_image, self.sensitivity)
            if result_image is None or original_image is None:
                raise ValueError("Image comparison failed.")
            QMetaObject.invokeMethod(self.parent, "compareFinished", Qt.QueuedConnection,
                                     Q_ARG(object, result_image), Q_ARG(object, original_image))
        except Exception as e:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection, Q_ARG(str, f"Comparison failed: {e}"))
