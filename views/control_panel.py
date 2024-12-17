from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QSlider)
from PyQt5.QtCore import Qt, pyqtSignal
import logging
from config.settings import (DEFAULT_SENSITIVITY, SLIDER_MIN, SLIDER_MAX)

class ControlPanel(QWidget):
    compare_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    print_clicked = pyqtSignal()
    sensitivity_released = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        # Poprzednio 275 px, teraz +150 px = 425 px szerokości panelu kontrolnego.
        self.setFixedWidth(425)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(5)
        self.setLayout(main_layout)

        # Przyciski:
        # 3 odstępy po 5 px =15 px
        # 425 -15=410 px na 4 przyciski
        # 410/4=102.5 px
        # Ustalamy: 2 przyciski po 102 px i 2 po 103 px:
        # 102+103+102+103=410 px idealnie
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        self.compare_btn = self._create_button("Compare", self.compare_clicked, 102)
        self.reset_btn = self._create_button("Reset", self.reset_clicked, 103)
        self.clear_btn = self._create_button("Clear", self.clear_clicked, 102)
        self.print_btn = self._create_button("Print", self.print_clicked, 103)

        buttons_layout.addWidget(self.compare_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.print_btn)

        main_layout.addLayout(buttons_layout)

        # Suwak:
        # 2 odstępy po 5 px =10 px
        # 425 -10=415 px na elementy
        # Etykieta=80 px, wartość=30 px razem 110 px
        # 415 -110=305 px na suwak
        sensitivity_layout = QHBoxLayout()
        sensitivity_layout.setSpacing(5)
        self.sensitivity_label = QLabel("Sensitivity:")
        self.sensitivity_label.setFixedWidth(80)
        self.sensitivity_value = QLabel(f"{DEFAULT_SENSITIVITY:03d}")
        self.sensitivity_value.setFixedWidth(30)
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(SLIDER_MIN)
        self.sensitivity_slider.setMaximum(SLIDER_MAX)
        self.sensitivity_slider.setValue(DEFAULT_SENSITIVITY)
        self.sensitivity_slider.setFixedWidth(305)

        self.sensitivity_slider.valueChanged.connect(self._on_sensitivity_changed)
        self.sensitivity_slider.sliderReleased.connect(self._on_sensitivity_released)

        sensitivity_layout.addWidget(self.sensitivity_label)
        sensitivity_layout.addWidget(self.sensitivity_slider)
        sensitivity_layout.addWidget(self.sensitivity_value)

        main_layout.addLayout(sensitivity_layout)

    def _create_button(self, text: str, slot, width: int) -> QPushButton:
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        btn.setFixedWidth(width)
        return btn

    def _on_sensitivity_changed(self, value: int):
        self.sensitivity_value.setText(f"{value:03d}")

    def _on_sensitivity_released(self):
        self.sensitivity_released.emit(self.get_sensitivity())

    def get_sensitivity(self) -> int:
        return self.sensitivity_slider.value()

    def set_sensitivity(self, value: int):
        self.sensitivity_slider.setValue(value)
