from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtCore import QRectF, Qt

class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(GraphicsView, self).__init__(scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self._zoom = 0
        self._empty = True
        self._scene = scene
        self._photo = None

    def fitImageInView(self, scale=True):
        try:
            if self._photo is None:
                return
            print("Fitting image in view.")
            self.resetTransform()
            rect = self._photo.boundingRect()
            if rect.isNull():
                return
            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self._zoom = 0
            print("Image fitted in view.")
        except Exception as e:
            print(f"An error occurred in fitImageInView: {e}")

    def hasPhoto(self):
        return not self._empty

    def setPhoto(self, pixmap=None):
        try:
            print(f"Setting photo. Pixmap is None: {pixmap is None}")
            if pixmap is None or pixmap.isNull():
                self._empty = True
                if self._photo:
                    print("Removing existing photo from scene.")
                    self._scene.removeItem(self._photo)
                    self._photo = None
                print("Clearing scene.")
                self._scene.clear()
            else:
                self._empty = False
                if not self._photo:
                    print("Creating new QGraphicsPixmapItem.")
                    self._photo = QGraphicsPixmapItem()
                    self._scene.addItem(self._photo)
                print("Setting pixmap to QGraphicsPixmapItem.")
                self._photo.setPixmap(pixmap)
                self.fitImageInView()
            print("Photo set successfully.")
        except Exception as e:
            print(f"An error occurred while setting photo: {e}")

    def wheelEvent(self, event: QWheelEvent):
        try:
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
        except Exception as e:
            print(f"An error occurred in wheelEvent: {e}")

    def mousePressEvent(self, event: QMouseEvent):
        try:
            if self._photo is not None:
                if event.button() == Qt.LeftButton:
                    self.setDragMode(QGraphicsView.ScrollHandDrag)
                elif event.button() == Qt.RightButton:
                    self.setDragMode(QGraphicsView.NoDrag)
            super(GraphicsView, self).mousePressEvent(event)
        except Exception as e:
            print(f"An error occurred in mousePressEvent: {e}")
