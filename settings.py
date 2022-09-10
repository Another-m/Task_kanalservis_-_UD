import os
from dotenv import load_dotenv

load_dotenv()


# Настройка обновления записей в БД:
#   Для полной синхронизации с таблицей True
#   Если нужно хранить, как архив, данные в бд, которые были удалены из таблицы - False
SYNCH_DATA = True

# Промежуток времени (секунд) между запросами к гугл таблице для проверки изменений в документе
TIME_REQUEST = 30

# Telegram
TOKEN = ""
ChatID = ""


# Путь к файлу с ключом к Google Sheets Api
PATH_TO_SECRET_KEY = 'credentials.json'
# Путь к таблице Google Sheets
G_TABLE = os.getenv("G_TABLE")


# Flask & Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


# Database config
DATABASE = os.getenv("DATABASE")
DRIVER = os.getenv("DRIVER")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")
NAME = os.getenv("NAME")
OWNER = os.getenv("OWNER")
PASSWORD = os.getenv("PASSWORD")
PG_CONFIG = f"{DATABASE}+{DRIVER}://{OWNER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"