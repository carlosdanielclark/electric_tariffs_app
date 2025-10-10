import os
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional


class ActivityLogger:
    """
    Sistema de registro de actividades sensibles en formato CSV.
    Diseñado para ser thread-safe, offline y resistente a fallos.
    """

    def __init__(self, log_path: Optional[str] = None) -> None:
        """
        Inicializa el logger con una ruta opcional de archivo.

        Args:
            log_path (Optional[str]): Ruta al archivo CSV de logs.
                                      Si es None, usa 'logs/logs_actividad.csv'.
        """
        if log_path is None:
            self.log_path = Path("logs") / "logs_actividad.csv"
        else:
            self.log_path = Path(log_path)
        self.ensure_log_directory_and_file()

    def ensure_log_directory_and_file(self) -> None:
        """
        Crea el directorio de logs y el archivo CSV con encabezados si no existen.
        """
        log_dir = self.log_path.parent
        log_dir.mkdir(parents=True, exist_ok=True)

        if not self.log_path.exists():
            with open(self.log_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "usuario_id", "evento", "detalles"])

    def log_event(self, user_id: int, event: str, details: str = "") -> None:
        """
        Registra un evento en el archivo CSV de forma segura.

        Args:
            user_id (int): ID del usuario que generó el evento.
            event (str): Nombre del evento (ej: 'registro_lectura', 'eliminacion_usuario').
            details (str): Información adicional opcional.

        Raises:
            ValueError: Si los parámetros son inválidos.
        """
        if user_id <= 0:
            raise ValueError("user_id debe ser un entero positivo.")
        if not event or not isinstance(event, str):
            raise ValueError("event debe ser una cadena no vacía.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, user_id, event, details])
        except Exception as e:
            # Fallback seguro: no detiene la app, pero registra en stderr
            print(f"[ERROR LOG] No se pudo escribir en {self.log_path}: {e}", flush=True)