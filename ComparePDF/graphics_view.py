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
            self.setScene(self._scene)
            self._photo = QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._photo)
        else:
            self._empty = True
            self._scene.clear()
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
