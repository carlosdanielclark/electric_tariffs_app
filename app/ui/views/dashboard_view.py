from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from decimal import Decimal

class DashboardView(QWidget):
    def __init__(self, user_id: int, reading_service) -> None:
        super().__init__()
        self.user_id = user_id
        self.reading_service = reading_service
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Fecha", "Lectura Actual", "Consumo", "Costo", "Eliminar"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self) -> None:
        readings = self.reading_service.get_all_readings_by_user(self.user_id)
        self.table.setRowCount(len(readings))
        for row, r in enumerate(reversed(readings)):  # Últimos primero
            self.table.setItem(row, 0, QTableWidgetItem(r.fecha.strftime("%Y-%m-%d %H:%M")))
            self.table.setItem(row, 1, QTableWidgetItem(f"{r.lectura_actual:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{r.consumo:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"${r.costo:.2f}"))

            delete_btn = QPushButton("Eliminar")
            delete_btn.setStyleSheet("background-color: #ff4d4d; color: white;")
            delete_btn.clicked.connect(lambda _, rid=r.id: self.delete_reading(rid))
            self.table.setCellWidget(row, 4, delete_btn)

    def delete_reading(self, reading_id: int) -> None:
        reply = QMessageBox.question(
            self, "Confirmar", "¿Eliminar esta lectura?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.reading_service.delete_reading(reading_id)
            self.load_data()