import os
from dotenv import load_dotenv

load_dotenv()  # читает .env и добавляет переменные в os.environ

DB_USER = os.getenv("DB_USER")        # получает значение DB_USER
DB_PASSWORD = os.getenv("DB_PASSWORD") # получает значение DB_PASSWORD
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")  # "localhost" — значение по умолчанию
DB_PORT = os.getenv("DB_PORT", "5432")

# Собирает строку подключения к БД
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Отладочный вывод
print(f"DB_USER = {repr(DB_USER)}")
print(f"DB_PASSWORD = {repr(DB_PASSWORD)}")
print(f"DB_NAME = {repr(DB_NAME)}")
print(f"DB_HOST = {repr(DB_HOST)}")
print(f"DATABASE_URL length = {len(DATABASE_URL)}")
print(f"DATABASE_URL first 80 chars = {DATABASE_URL[:80]}")