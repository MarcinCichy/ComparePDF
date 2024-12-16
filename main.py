import sys
import os
import traceback
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject, pyqtSlot

# Dodaj ścieżkę do katalogu głównego projektu do PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from views.main_window import MainWindow
from controllers.pdf_controller import PDFController
from config.settings import MSG_ERROR_GENERAL


def setup_logging():
    """Konfiguracja systemu logowania."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("pdf_comparer.log"),
            logging.StreamHandler()
        ]
    )


def handle_exception(exc_type, exc_value, exc_traceback):
    """Globalny handler wyjątków."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.critical(f"Unhandled exception: {error_msg}")

    if QApplication.instance():
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Critical Error",
                             MSG_ERROR_GENERAL.format(error_msg))


def main():
    try:
        setup_logging()
        logging.info("Starting application...")
        sys.excepthook = handle_exception

        app = QApplication(sys.argv)
        logging.info("Creating controller...")
        controller = PDFController()
        logging.info("Creating main window...")
        main_window = MainWindow(controller)
        logging.info("Setting view...")
        controller.set_view(main_window)

        main_window.show()
        logging.info("Application started successfully")
        sys.exit(app.exec_())
    except Exception as e:
        logging.critical(f"Failed to start application: {e}")
        raise

if __name__ == '__main__':
    main()