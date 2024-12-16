from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLabel,
                             QSlider, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
import logging
from config.settings import (DEFAULT_SENSITIVITY, SLIDER_MIN, SLIDER_MAX)

class ControlPanel(QWidget):
    """Panel kontrolny aplikacji."""

    # Sygnały
    compare_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    print_clicked = pyqtSignal()
    sensitivity_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Konfiguracja UI komponentu."""
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Kontrolka czułości
        sensitivity_container = QWidget()
        sensitivity_layout = QHBoxLayout()

        self.sensitivity_label = QLabel("Sensitivity:")
        self.sensitivity_value = QLabel(f"{DEFAULT_SENSITIVITY:03d}")
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(SLIDER_MIN)
        self.sensitivity_slider.setMaximum(SLIDER_MAX)
        self.sensitivity_slider.setValue(DEFAULT_SENSITIVITY)

        self.sensitivity_slider.valueChanged.connect(self._on_sensitivity_changed)

        sensitivity_layout.addWidget(self.sensitivity_label)
        sensitivity_layout.addWidget(self.sensitivity_slider)
        sensitivity_layout.addWidget(self.sensitivity_value)
        sensitivity_container.setLayout(sensitivity_layout)

        # Przyciski
        self.compare_btn = self._create_button("Compare", self.compare_clicked)
        self.reset_btn = self._create_button("Reset", self.reset_clicked)
        self.clear_btn = self._create_button("Clear", self.clear_clicked)
        self.print_btn = self._create_button("Print", self.print_clicked)

        # Ustawiamy minimalną szerokość, aby przyciski były szersze
        for btn in [self.compare_btn, self.reset_btn, self.clear_btn, self.print_btn]:
            btn.setMinimumWidth(80)

        # Dodanie elementów do głównego layoutu
        layout.addWidget(sensitivity_container)
        layout.addWidget(self.compare_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.print_btn)

        # Dodanie elastycznego spacera
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum))

    def _create_button(self, text: str, slot) -> QPushButton:
        """Tworzy przycisk z podłączonym slotem."""
        btn = QPushButton(text)
        btn.clicked.connect(slot)
        return btn

    def _on_sensitivity_changed(self, value: int):
        """Obsługa zmiany wartości suwaka czułości."""
        try:
            self.sensitivity_value.setText(f"{value:03d}")
            self.sensitivity_changed.emit(value)
        except Exception as e:
            logging.error(f"Error in sensitivity change: {e}")

    def get_sensitivity(self) -> int:
        """Zwraca aktualną wartość czułości."""
        return self.sensitivity_slider.value()

    def set_sensitivity(self, value: int):
        """Ustawia wartość czułości."""
        self.sensitivity_slider.setValue(value)
