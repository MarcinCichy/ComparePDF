import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Główny widget i układ
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Lewa część: Opcje
        self.optionsLayout = QVBoxLayout()

        # Combo box dla gatunków stali
        self.steelTypeComboBox = QComboBox()
        self.steelTypeComboBox.addItems(["czarna", "nierdzewna", "aluminium"])
        self.steelTypeComboBox.setMaximumWidth(80)
        self.optionsLayout.addWidget(QLabel("Gatunek stali:"))
        self.optionsLayout.addWidget(self.steelTypeComboBox)

        # Combo box dla grubości blachy
        self.sheetThicknessComboBox = QComboBox()
        self.sheetThicknessComboBox.addItems(["0,5", "0,8", "1", "1,5", "2", "2,5", "3", "4", "5", "6", "8", "10"])
        self.steelTypeComboBox.setMaximumWidth(40)
        self.optionsLayout.addWidget(QLabel("Grubość blachy:"))
        self.optionsLayout.addWidget(self.sheetThicknessComboBox)

        # Combo box dla wyboru matrycy
        self.matrixChoiceComboBox = QComboBox()
        self.matrixChoiceComboBox.addItems(["V10", "V16", "V24", "V50", "V63"])
        self.steelTypeComboBox.setMaximumWidth(40)
        self.optionsLayout.addWidget(QLabel("Matryca:"))
        self.optionsLayout.addWidget(self.matrixChoiceComboBox)

        self.optionsLayout.addStretch()  # Dodatkowa przestrzeń na dole
        # Środkowa część: Wyświetlanie rysunków
        self.displayLayout = QVBoxLayout()
        self.displayLabel = QLabel("Wyświetlacz rysunków DXF")
        self.displayLayout.addWidget(self.displayLabel)
        self.displayLayout.addStretch()  # Pozwala na rozciąganie się pionowo

        # Prawa część: Lista rysunków
        self.dxfList = QListWidget()
        self.dxfList.addItems(["Rysunek1.dxf", "Rysunek2.dxf"])  # Przykładowe dane

        # Dodajemy sekcje do głównego układu z proporcjami
        self.mainLayout.addLayout(self.optionsLayout, 1)  # Opcje (1 część)
        self.mainLayout.addLayout(self.displayLayout, 3)  # Wyświetlanie (3 części)
        self.mainLayout.addWidget(self.dxfList, 1)       # Lista rysunków (1 część)

        # Ustawienia okna
        self.setWindowTitle("Przeglądarka rysunków DXF")
        self.resize(800, 600)  # Startowy rozmiar okna

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
