from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

class ReadingFormWidget(QWidget):
    reading_submitted = pyqtSignal(float, float)

    def __init__(self, previous_reading: float = 0.0) -> None:
        super().__init__()
        self.previous_reading = previous_reading
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.previous_label = QLabel("Lectura Anterior")
        self.previous_input = QLineEdit()
        self.previous_input.setText(f"{self.previous_reading:.2f}")
        self.previous_input.setReadOnly(True)
        self.previous_input.setPlaceholderText("0.00")

        self.current_label = QLabel("Lectura Actual")
        self.current_input = QLineEdit()
        self.current_input.setPlaceholderText("Ingrese lectura actual")

        self.save_button = QPushButton("Guardar Lectura")
        self.save_button.clicked.connect(self.on_save)

        layout.addWidget(self.previous_label)
        layout.addWidget(self.previous_input)
        layout.addWidget(self.current_label)
        layout.addWidget(self.current_input)
        layout.addWidget(self.save_button)
        layout.addStretch()

        self.setLayout(layout)

    def on_save(self) -> None:
        try:
            current = float(self.current_input.text())
            previous = float(self.previous_input.text())
            if current <= previous:
                return  # Validación básica; se manejará en ViewModel
            self.reading_submitted.emit(previous, current)
            self.current_input.clear()
        except ValueError:
            pass  # Manejo de error en capa superior