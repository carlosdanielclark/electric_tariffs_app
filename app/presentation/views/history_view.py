from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from collections import defaultdict
from datetime import datetime

class HistoryView(QWidget):
    def __init__(self, user_id: int, reading_service) -> None:
        super().__init__()
        self.user_id = user_id
        self.reading_service = reading_service
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Mes", "Consumo Total", "Costo Total", "Lecturas"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self) -> None:
        readings = self.reading_service.get_all_readings_by_user(self.user_id)
        monthly = defaultdict(lambda: {"consumo": 0.0, "costo": 0.0, "count": 0})

        for r in readings:
            key = r.fecha.strftime("%Y-%m")
            monthly[key]["consumo"] += float(r.consumo)
            monthly[key]["costo"] += float(r.costo)
            monthly[key]["count"] += 1

        months = sorted(monthly.keys(), reverse=True)
        self.table.setRowCount(len(months))
        for row, month in enumerate(months):
            data = monthly[month]
            self.table.setItem(row, 0, QTableWidgetItem(month))
            self.table.setItem(row, 1, QTableWidgetItem(f"{data['consumo']:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"${data['costo']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(data["count"])))