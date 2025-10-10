from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # OK en PyQt6
from matplotlib.figure import Figure
from collections import defaultdict


class GraphView(QWidget):
    def __init__(self, user_id: int, reading_service) -> None:
        super().__init__()
        self.user_id = user_id
        self.reading_service = reading_service
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def load_data(self) -> None:
        readings = self.reading_service.get_all_readings_by_user(self.user_id)
        monthly = defaultdict(lambda: {"consumo": 0.0, "costo": 0.0})

        for r in readings:
            key = r.fecha.strftime("%Y-%m")
            monthly[key]["consumo"] += float(r.consumo)
            monthly[key]["costo"] += float(r.costo)

        sorted_items = sorted(monthly.items())
        if not sorted_items:
            return

        months = [item[0].split("-")[1] for item in sorted_items]
        consumos = [item[1]["consumo"] for item in sorted_items]
        costos = [item[1]["costo"] for item in sorted_items]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(months, consumos, color="#00C8D6")

        for bar, costo in zip(bars, costos):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + max(consumos) * 0.01,
                f"${costo:.2f}",
                ha='center', va='bottom', fontweight='bold'
            )

        ax.set_ylabel("Consumo (kWh)")
        ax.set_title("Consumo Mensual")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.canvas.draw()