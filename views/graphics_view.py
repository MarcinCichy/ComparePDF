from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent, QPixmap
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
import logging
from config.settings import ZOOM_FACTOR_IN, ZOOM_FACTOR_OUT

class GraphicsView(QGraphicsView):
    """Widok do wyświetlania i manipulacji obrazami."""

    # Sygnały
    zoom_changed = pyqtSignal(int)

    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene or QGraphicsScene())
        self._setup_ui()
        self._init_variables()

    def _setup_ui(self):
        """Konfiguracja UI komponentu."""
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def _init_variables(self):
        """Inicjalizacja zmiennych instancji."""
        self._zoom = 0
        self._empty = True
        self._scene = self.scene()
        self._photo = None
        self._pixmap = None

    def fitImageInView(self, scale=True):
        """Dopasowuje obraz do widoku."""
        try:
            if not self._photo:
                return

            self.setUpdatesEnabled(False)
            self.resetTransform()
            rect = self._photo.boundingRect()
            if rect.isNull():
                return

            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                         viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self._zoom = 0
            self.zoom_changed.emit(self._zoom)

        except Exception as e:
            logging.error(f"Error in fitImageInView: {e}")
        finally:
            self.setUpdatesEnabled(True)

    def setPhoto(self, pixmap: QPixmap = None):
        """Ustawia obraz do wyświetlenia."""
        try:
            self._zoom = 0
            if pixmap and not pixmap.isNull():
                self._empty = False
                if not self._photo:
                    self._photo = QGraphicsPixmapItem()
                    self._scene.addItem(self._photo)
                self._pixmap = pixmap
                self._photo.setPixmap(self._pixmap)
                self.fitImageInView()
            else:
                self._empty = True
                if self._photo:
                    self._scene.removeItem(self._photo)
                    self._photo = None
                self._scene.clear()

        except Exception as e:
            logging.error(f"Error in setPhoto: {e}")

    def wheelEvent(self, event: QWheelEvent):
        """Obsługa zoomu kółkiem myszy."""
        try:
            if self.hasPhoto():
                if event.angleDelta().y() > 0:
                    factor = ZOOM_FACTOR_IN
                    self._zoom += 1
                else:
                    factor = ZOOM_FACTOR_OUT
                    self._zoom -= 1

                if self._zoom > 0:
                    self.scale(factor, factor)
                elif self._zoom == 0:
                    self.fitImageInView()
                else:
                    self._zoom = 0

                self.zoom_changed.emit(self._zoom)

        except Exception as e:
            logging.error(f"Error in wheelEvent: {e}")

    def mousePressEvent(self, event: QMouseEvent):
        """Obsługa kliknięć myszy."""
        try:
            if self._photo:
                if event.button() == Qt.LeftButton:
                    self.setDragMode(QGraphicsView.ScrollHandDrag)
                elif event.button() == Qt.RightButton:
                    self.setDragMode(QGraphicsView.NoDrag)
            super().mousePressEvent(event)
        except Exception as e:
            logging.error(f"Error in mousePressEvent: {e}")

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Obsługa puszczenia przycisku myszy."""
        try:
            super().mouseReleaseEvent(event)
            self.setDragMode(QGraphicsView.NoDrag)
        except Exception as e:
            logging.error(f"Error in mouseReleaseEvent: {e}")

    def hasPhoto(self):
        """Sprawdza czy jest wyświetlany obraz."""
        return not self._empty
