from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox


class UserStatsView(QWidget):
    def __init__(self, user_service) -> None:
        super().__init__()
        self.user_service = user_service
        self.setup_ui()
        self.load_data()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.active_label = QLabel("Usuarios registrados: 0")
        self.deleted_label = QLabel("Usuarios eliminados: 0")
        self.active_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.deleted_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.active_label)
        layout.addWidget(self.deleted_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Usuario", "Eliminar"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        layout.addStretch()
        self.setLayout(layout)

    def load_data(self) -> None:
        users = self.user_service.get_all_users()
        deleted_count = self.user_service.get_deleted_user_count()
        self.active_label.setText(f"Usuarios registrados: {len(users)}")
        self.deleted_label.setText(f"Usuarios eliminados: {deleted_count}")

        self.table.setRowCount(len(users))
        for row, u in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(u.id)))
            self.table.setItem(row, 1, QTableWidgetItem(u.nombre))
            self.table.setItem(row, 2, QTableWidgetItem(u.username))

            delete_btn = QPushButton("Eliminar")
            delete_btn.setStyleSheet("background-color: #ff4d4d; color: white;")
            delete_btn.clicked.connect(lambda _, uid=u.id: self.delete_user(uid))
            self.table.setCellWidget(row, 3, delete_btn)

    def delete_user(self, user_id: int) -> None:
        reply = QMessageBox.question(
            self, "Confirmar", "¿Eliminar este usuario y sus datos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.user_service.delete_user(user_id)
            self.load_data()