import pytest
pytest.importorskip("PyQt6")
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QApplication


def test_app_starts(qtbot: QtBot) -> None:
    app = QApplication.instance() or QApplication([])
    from src.presentation.views.main_window import MainWindow
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()
    assert w.windowTitle() == "Electric Tariffs App"