from PyQt6.QtCore import QObject, pyqtSignal as Signal
from decimal import Decimal


class ReadingViewModel(QObject):
    reading_saved = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, user_id: int, reading_service) -> None:
        super().__init__()
        self.user_id = user_id
        self.reading_service = reading_service
        self._last_reading: float = 0.0

    def load_last_reading(self) -> None:
        last = self.reading_service.get_last_reading_by_user(self.user_id)
        self._last_reading = float(last.lectura_actual) if last else 0.0

    def get_last_reading(self) -> float:
        return self._last_reading

    def save_reading(self, previous: float, current: float) -> None:
        if current <= previous:
            self.error_occurred.emit("La lectura actual debe ser mayor que la anterior.")
            return
        try:
            reading = self.reading_service.register_reading(
                user_id=self.user_id,
                lectura_actual=current,
                lectura_anterior=previous
            )
            self.reading_saved.emit(reading)
        except Exception as e:
            self.error_occurred.emit(f"Error al guardar: {str(e)}")