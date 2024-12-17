import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from controllers.pdf_controller import PDFController
from views.main_window import MainWindow
from config.settings import get_dark_palette, QSS  # importujemy z pliku settings

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Ustawienie palety z settings.py
    palette = get_dark_palette()
    app.setPalette(palette)

    # Ustawienie QSS z pliku settings.py
    app.setStyleSheet(QSS)

    controller = PDFController()
    window = MainWindow(controller)
    controller.set_view(window)
    window.show()
    sys.exit(app.exec_())
