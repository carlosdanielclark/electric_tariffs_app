from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QDoubleSpinBox, QPushButton, QMessageBox


class ConfigView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        title = QLabel("Configuración")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.cargo_fijo = QDoubleSpinBox()
        self.cargo_fijo.setPrefix("$ ")
        self.cargo_fijo.setRange(0, 1000)
        self.cargo_fijo.setValue(0.0)

        self.impuesto = QDoubleSpinBox()
        self.impuesto.setSuffix(" %")
        self.impuesto.setRange(0, 100)
        self.impuesto.setValue(0.0)

        save_btn = QPushButton("Guardar ajustes")
        save_btn.clicked.connect(self.on_save)

        layout.addWidget(QLabel("Cargo fijo ($):"))
        layout.addWidget(self.cargo_fijo)
        layout.addWidget(QLabel("Impuesto (%):"))
        layout.addWidget(self.impuesto)
        layout.addWidget(save_btn)
        self.setLayout(layout)
        self.setFixedWidth(380)

    def on_save(self) -> None:
        cargo = self.cargo_fijo.value()
        impuesto_pct = self.impuesto.value() / 100.0
        QMessageBox.information(self, "Guardado", f"Cargo fijo: ${cargo}, Impuesto: {impuesto_pct*100:.2f}%")