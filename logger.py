from datetime import datetime
from pathlib import Path

from config import APP_DIR


LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def log(component, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] [{component}] {message}"

    print(line)

    try:
        with open(LOG_FILE, "a", encoding="utf8") as f:
            f.write(line + "\n")
    except Exception:
        pass