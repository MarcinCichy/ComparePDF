import sys
from PyQt5.QtWidgets import QApplication
from pdf_comparer import PDFComparer


def main():
    app = QApplication(sys.argv)
    ex = PDFComparer()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
