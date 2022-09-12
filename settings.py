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
G_TABLE = https://docs.google.com/spreadsheets/d/1iidER40PNhBhtWDyUMdTvr5FoSJUr7rftr4t4IltMxE/edit?usp=sharing


# Flask & Celery
CELERY_BROKER_URL = redis://localhost:6379/1
CELERY_RESULT_BACKEND = redis://localhost:6379/2


# Database config
DATABASE = postgresql
DRIVER = psycopg2
PORT = 5431
HOST = localhost
NAME = app
OWNER = postgres
PASSWORD = 123
PG_CONFIG = f"{DATABASE}+{DRIVER}://{OWNER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
