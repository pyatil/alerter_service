import os


WEB_PORT = os.environ.get("WEB_PORT", "8000")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DATA_PATH = os.path.join(os.path.curdir, "var")
