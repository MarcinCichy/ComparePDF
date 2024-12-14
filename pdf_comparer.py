import gc
import logging
import fitz  # Upewnij się, że importujesz fitz
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
                             QRadioButton, QSpacerItem, QSizePolicy, QFileDialog, QGraphicsScene,
                             QFrame, QButtonGroup, QSlider, QMessageBox, QProgressDialog)
from PyQt5.QtCore import (Qt, QRunnable, QThreadPool, pyqtSlot, QMetaObject, Q_ARG)
from PyQt5.QtGui import QPixmap, QImage, QPainter
from utils import pil2qimage, pdf_to_image, compare_images
from graphics_view import GraphicsView
import concurrent.futures

MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB

# Konfiguracja loggera
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


class PDFLoadTask(QRunnable):
    def __init__(self, callback, file_path, num, parent, timeout=15):
        super().__init__()
        self.callback = callback
        self.file_path = file_path
        self.num = num
        self.parent = parent
        self.timeout = timeout  # Limit czasu w sekundach

    def run(self):
        try:
            print(f"Loading PDF file: {self.file_path}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.load_pdf)
                pixmap = future.result(timeout=self.timeout)
                QMetaObject.invokeMethod(self.parent, "loadFinished", Qt.QueuedConnection,
                                         Q_ARG(QPixmap, pixmap), Q_ARG(int, self.num))
        except concurrent.futures.TimeoutError:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection,
                                     Q_ARG(str, f"Loading PDF file timed out after {self.timeout} seconds."))
        except Exception as e:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection,
                                     Q_ARG(str, f"Failed to load or process PDF file: {e}"))

    def load_pdf(self):
        with fitz.open(self.file_path) as doc:
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
        return pixmap


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
        self.progress_dialog = None
        self.compare_task = None
        self.result_qimage = None
        self.result_pixmap = None
        self.original_qimage = None
        self.original_pixmap = None
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setWindowTitle('PDF Comparator v2.0')
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
                self.progress_dialog = QProgressDialog("Comparing PDFs...", "Cancel", 0, 0, self)
                self.progress_dialog.setWindowModality(Qt.WindowModal)
                self.progress_dialog.canceled.connect(self.on_cancel_compare)
                self.progress_dialog.show()

                self.compare_task = ImageCompareTask(base_file, compare_file, self.sensitivity, self.compareFinished, self)
                QThreadPool.globalInstance().start(self.compare_task)
            else:
                QMessageBox.warning(self, "File Error", "Please upload both PDF files.")
        except Exception as e:
            error_msg = f"An error occurred: {e}."
            self.showError(error_msg)

    def on_cancel_compare(self):
        if self.compare_task:
            self.compare_task.cancel()
        self.showError("Comparison canceled by user.")
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

    @pyqtSlot(object, object)
    def compareFinished(self, result_image, original_image):
        if self.progress_dialog:
            # Odłącz sygnał 'canceled' przed zamknięciem dialogu
            self.progress_dialog.canceled.disconnect(self.on_cancel_compare)
            self.progress_dialog.close()
            self.progress_dialog = None
        try:
            logging.debug("compareFinished called.")
            if result_image and original_image:
                logging.debug("Images are valid.")

                # Konwertuj obrazy do "RGBA" przed konwersją na QImage
                result_image = result_image.convert("RGBA")
                original_image = original_image.convert("RGBA")

                self.result_qimage = pil2qimage(result_image)

                if self.result_qimage is None or self.result_qimage.isNull():
                    self.showError("Failed to convert result image to QImage.")
                    return

                image_size = self.result_qimage.sizeInBytes()
                print(f'IMAGE SIZE AFTER CONVERSION = {image_size / (1024 * 1024):.2f} MB')
                logging.debug(f"Result image size: {image_size} bytes.")

                if image_size > MAX_IMAGE_SIZE:
                    self.showError(
                        f"Resulting image is too large to display ({image_size / (1024 * 1024):.2f} MB). Please reduce the sensitivity or try smaller PDFs.")
                    return

                self.result_pixmap = QPixmap.fromImage(self.result_qimage)
                if self.result_pixmap.isNull():
                    self.showError("Failed to create QPixmap from QImage.")
                    return

                self.view.setPhoto(self.result_pixmap)

                # Przechowujemy oryginalny obraz
                self.original_qimage = pil2qimage(original_image)
                self.original_pixmap = QPixmap.fromImage(self.original_qimage)

                gc.collect()
                logging.debug("Garbage collection completed after setting photo.")
            else:
                self.showError("Failed to generate comparison results.")
        except Exception as e:
            logging.error(f"Error displaying comparison results: {e}")
            self.showError(f"Error displaying comparison results: {e}")
            gc.collect()
            logging.debug("Garbage collection completed after exception.")

    def on_reset_clicked(self):
        if self.previewLabel1 and self.previewLabel2:
            self.previewLabel1.clear()
            self.previewLabel2.clear()
        self.file1, self.file2 = None, None
        if self.view:
            self.view.setPhoto(None)

    def on_clear_clicked(self):
        if hasattr(self, 'original_pixmap'):
            self.view.setPhoto(self.original_pixmap)

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
    def __init__(self, base_file, compare_file, sensitivity, callback, parent, timeout=30):
        super().__init__()
        self.base_file = base_file
        self.compare_file = compare_file
        self.sensitivity = sensitivity
        self.callback = callback
        self.parent = parent
        self.timeout = timeout  # Limit czasu w sekundach
        self._is_canceled = False

    def cancel(self):
        self._is_canceled = True

    def run(self):
        try:
            print(f"Comparing images: {self.base_file} vs {self.compare_file}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.compare_images)
                result = future.result(timeout=self.timeout)
                if result is None:
                    return
                result_image, original_image = result
                QMetaObject.invokeMethod(self.parent, "compareFinished", Qt.QueuedConnection,
                                         Q_ARG(object, result_image), Q_ARG(object, original_image))
        except concurrent.futures.TimeoutError:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection,
                                     Q_ARG(str, f"Image comparison timed out after {self.timeout} seconds."))
        except Exception as e:
            QMetaObject.invokeMethod(self.parent, "showError", Qt.QueuedConnection,
                                     Q_ARG(str, f"Comparison failed: {e}"))

    def compare_images(self):
        if self._is_canceled:
            return None
        base_image = pdf_to_image(self.base_file)
        if base_image is None:
            raise ValueError(f"Failed to convert {self.base_file} to image.")
        if self._is_canceled:
            return None
        compare_image = pdf_to_image(self.compare_file)
        if compare_image is None:
            raise ValueError(f"Failed to convert {self.compare_file} to image.")
        if self._is_canceled:
            return None
        result_image, original_image = compare_images(base_image, compare_image, self.sensitivity)
        if result_image is None or original_image is None:
            raise ValueError("Image comparison failed.")
        return result_image, original_image

