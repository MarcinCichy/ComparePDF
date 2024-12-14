import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from pdf_comparer import PDFComparer


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    QMessageBox.critical(None, "Application Error", f"An unexpected error occurred:\n{error_msg}")


sys.excepthook = handle_exception


def main():
    app = QApplication(sys.argv)
    ex = PDFComparer()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
