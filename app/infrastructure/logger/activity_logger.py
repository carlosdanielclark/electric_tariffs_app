from __future__ import annotations
import os, csv
from datetime import datetime
from app.config import settings


class ActivityLogger:
    def __init__(self, log_path: str | None = None):
        base = log_path or (settings.LOGS_DIR / "logs_actividad.csv")
        self.log_path = str(base)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "usuario_id", "evento", "detalles"])

    def log_event(self, user_id: int | None, event: str, details: str = "") -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([ts, user_id, event, details])
        except Exception as e:
            # fallback simple print
            print(f"Error escribiendo log: {e}")
