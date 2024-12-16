from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QMessageBox,
                            QProgressDialog)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
import logging
from views.preview_panel import PreviewPanel
from views.control_panel import ControlPanel
from views.graphics_view import GraphicsView
from config.settings import WINDOW_TITLE


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        self._connect_signals()
        self.progress_dialog = None

    def _setup_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

        self.preview_panel = PreviewPanel()
        self.graphics_view = GraphicsView()
        self.control_panel = ControlPanel()

        # Dodajemy panel podglądu po lewej
        self.main_layout.addWidget(self.preview_panel)
        # Dodajemy widok graficzny po prawej
        self.main_layout.addWidget(self.graphics_view)
        # Dodajemy panel kontrolny do layoutu podglądu, aby znalazł się pod podglądami PDF
        self.preview_panel.layout.addWidget(self.control_panel)

        # Ustawiamy proporcje (stretch) pomiędzy panelami
        # np. preview_panel : graphics_view = 1 : 4
        self.main_layout.setStretch(0, 1)  # Pierwszy widget (preview_panel)
        self.main_layout.setStretch(1, 4)  # Drugi widget (graphics_view)

        self.showMaximized()

    def _connect_signals(self):
        try:
            # Sygnały z PreviewPanel
            self.preview_panel.file_clicked.connect(self.controller.load_file)
            self.preview_panel.base_changed.connect(self.controller.set_base_document)

            # Sygnały z ControlPanel
            self.control_panel.compare_clicked.connect(self.controller.compare_documents)
            self.control_panel.reset_clicked.connect(self.controller.reset)
            self.control_panel.clear_clicked.connect(self.controller.clear)
            self.control_panel.print_clicked.connect(self.print_result)
            self.control_panel.sensitivity_changed.connect(self.controller.set_sensitivity)
        except Exception as e:
            logging.error(f"Error connecting signals: {e}")
            raise

    def show_progress(self, message: str):
        """Pokazuje dialog postępu."""
        self.progress_dialog = QProgressDialog(message, "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(500)
        self.progress_dialog.canceled.connect(self.controller.cancel_operation)
        self.progress_dialog.show()

    def hide_progress(self):
        """Ukrywa dialog postępu."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

    def show_error(self, message: str):
        """Wyświetla komunikat o błędzie."""
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message: str):
        """Wyświetla komunikat informacyjny."""
        QMessageBox.information(self, "Information", message)

    def print_result(self):
        """Drukuje aktualny widok."""
        try:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec_() == QPrintDialog.Accepted:
                painter = QPainter(printer)
                self.graphics_view.render(painter)
                painter.end()
        except Exception as e:
            logging.error(f"Error printing: {e}")
            self.show_error(f"Error printing: {str(e)}")
