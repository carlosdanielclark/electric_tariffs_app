from PyQt6.QtCore import QObject, pyqtSignal
from decimal import Decimal
from typing import Optional

class ReadingViewModel(QObject):
    reading_saved = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, user_id: int, reading_service) -> None:
        super().__init__()
        self.user_id = user_id
        self.reading_service = reading_service
        self._last_reading: Optional[float] = None

    def load_last_reading(self) -> None:
        last = self.reading_service.get_last_reading_by_user(self.user_id)
        if last:
            self._last_reading = last.lectura_actual
        else:
            self._last_reading = 0.0

    def get_last_reading(self) -> float:
        return self._last_reading or 0.0

    def save_reading(self, previous: float, current: float) -> None:
        if current <= previous:
            self.error_occurred.emit("La lectura actual debe ser mayor que la anterior.")
            return
        try:
            reading = self.reading_service.register_reading(
                user_id=self.user_id,
                lectura_actual=Decimal(str(current)),
                lectura_anterior=Decimal(str(previous))
            )
            self.reading_saved.emit(reading)
        except Exception as e:
            self.error_occurred.emit(f"Error al guardar: {str(e)}")