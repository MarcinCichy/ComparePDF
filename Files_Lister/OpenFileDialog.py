from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
from pathlib import Path


class OpenFileDialog (QMainWindow):

    def __init__(self):
        super().__init__()

        # open dialog
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        print(fname)
        # #if file selected, print text contents
        # if fname[0]:
        #         data = f.read()
        #         print(data)
        #         exit()

def main():
    app = QApplication(sys.argv)
    ex = OpenFileDialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()