from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # type: ignore
from matplotlib.axes import Axes  # type: ignore
import matplotlib.dates as mdates  # type: ignore
from app.domain.entities.user import User
from app.infrastructure.repositories.sqlite_reading_repository import SQLiteReadingRepository


class DashboardView(QWidget):
    def __init__(self, current_user: User, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.current_user = current_user
        self.reading_repo = SQLiteReadingRepository()
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.chart_selector = QComboBox()
        self.chart_selector.addItems(["Línea (tiempo)", "Barras (últimas lecturas)"])
        self.chart_selector.currentIndexChanged.connect(self.render_chart)
        header_layout.addWidget(self.chart_selector)
        layout.addLayout(header_layout)

        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)  # type: ignore
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas, stretch=3)

        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Lecturas recientes:"))
        layout.addWidget(self.list_widget, stretch=1)
        self.setLayout(layout)

    def load_data(self) -> None:
        items = self.reading_repo.get_by_user(self.current_user.id)
        self.readings = items
        self.render_chart()
        self.list_widget.clear()
        for r in items:
            ts = r.fecha.isoformat() if r.fecha else "sin fecha"
            consumo_str = f"{r.consumo:.2f}"
            costo_str = f"{r.costo:.2f}"
            self.list_widget.addItem(f"{ts} — Consumo: {consumo_str} kWh — Costo: ${costo_str}")

    def render_chart(self) -> None:
        readings = list(reversed(self.readings))
        self.figure.clf()
        ax: Axes = self.figure.add_subplot(111)  # type: ignore
        if not readings:
            ax.text(0.5, 0.5, "No hay datos de lecturas", ha="center", va="center")
            self.canvas.draw()  # type: ignore
            return

        dates = [r.fecha if r.fecha else datetime.now() for r in readings]
        date_nums = [mdates.date2num(d) for d in dates]  # ← mejor que timestamp()
        values = [float(r.consumo) for r in readings]

        if self.chart_selector.currentIndex() == 0:
            ax.plot(date_nums, values, marker="o", linewidth=2)
            ax.set_title("Consumo (kWh) vs Fecha")
            ax.set_ylabel("kWh")
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # type: ignore
            self.figure.autofmt_xdate()
        else:
            ax.bar(range(len(values)), values)
            ax.set_xticks(range(len(values)))
            ax.set_xticklabels([d.strftime("%Y-%m-%d") for d in dates], rotation=45, ha="right")
            ax.set_title("Consumo por lectura (últimas)")

        self.figure.tight_layout()
        self.canvas.draw()  # type: ignore