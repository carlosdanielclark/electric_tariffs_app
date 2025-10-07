from pathlib import Path

BASE_DIR = (
    Path(__file__).resolve().parents[2]
)  # project root (..../electric_tariffs_app)
DATA_DIR = BASE_DIR / "data"
DB_PATH = str(DATA_DIR / "app.db")
LOGS_DIR = BASE_DIR / "logs"
