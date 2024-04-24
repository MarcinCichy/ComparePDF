from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent, QPixmap
from PyQt5.QtCore import QRectF, Qt

from utils import pil2qimage


class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(GraphicsView, self).__init__(scene)
        self._zoom = 0
        self._empty = True
        self._scene = scene
        self._photo = None  # Obiekt dla głównego obrazu
        self._highlights = None  # Obiekt dla zaznaczeń

    def fitImageInView(self, scale=True):
        rect = self.sceneRect()
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def hasPhoto(self):
        return not self._empty

    def setPhoto(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self._empty = False
            if self._photo is not None:
                self._scene.removeItem(self._photo)
            self._photo = QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._photo)
        else:
            if self._photo is not None:
                self._scene.removeItem(self._photo)
                self._photo = None
            self._empty = True
        self.fitImageInView()

    def wheelEvent(self, event: QWheelEvent):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitImageInView()
            else:
                self._zoom = 0

    def mousePressEvent(self, event: QMouseEvent):
        if self._photo is not None:
            if event.button() == Qt.LeftButton:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            elif event.button() == Qt.RightButton:
                self.setDragMode(QGraphicsView.NoDrag)
        super(GraphicsView, self).mousePressEvent(event)

    def setHighlights(self, image):
        if image:
            if self._highlights:
                self._scene.removeItem(self._highlights)  # Usuń poprzednie zaznaczenia, jeśli istnieją
            q_img = pil2qimage(image)  # Konwertuje obraz PIL na QImage
            self._highlights = QGraphicsPixmapItem(QPixmap.fromImage(q_img))
            self._scene.addItem(self._highlights)
            print("Highlights added to the scene")
        else:
            print("No image provided for highlights")

    def clearHighlights(self):
        if self._highlights:
            self._scene.removeItem(self._highlights)
            self._highlights = None
            print("Highlights cleared")
        else:
            print("No highlights to clear")