from __future__ import annotations
from decimal import Decimal
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from app.application.services.reading_service import ReadingService, NewReading
from app.infrastructure.repositories.sqlite_reading_repository import SQLiteReadingRepository
from app.domain.entities.user import User

class ReadingForm(QWidget):
    def __init__(self, current_user: User, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.current_user = current_user
        self.reading_repo = SQLiteReadingRepository()
        self.service = ReadingService(reading_repo=self.reading_repo)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Registrar Lectura")
        layout = QVBoxLayout()
        title = QLabel("Registrar nueva lectura")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.input_anterior = QLineEdit()
        self.input_anterior.setPlaceholderText("Lectura anterior (kWh)")

        self.input_actual = QLineEdit()
        self.input_actual.setPlaceholderText("Lectura actual (kWh)")

        btn = QPushButton("Guardar lectura")
        btn.clicked.connect(self.on_save)

        layout.addWidget(self.input_anterior)
        layout.addWidget(self.input_actual)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.setFixedWidth(380)

    def on_save(self) -> None:
        try:
            anterior = Decimal(self.input_anterior.text().strip())
            actual = Decimal(self.input_actual.text().strip())
        except Exception:
            QMessageBox.warning(self, "Error", "Valores numéricos inválidos.")
            return

        try:
            reading = self.service.record_reading(
                NewReading(user_id=self.current_user.id, lectura_actual=actual, lectura_anterior=anterior)
            )
            QMessageBox.information(
                self, "Guardado", f"Lectura registrada. Consumo: {reading.consumo} kWh, Costo: ${reading.costo}"
            )
            self.input_anterior.clear()
            self.input_actual.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error inesperado: {e}")