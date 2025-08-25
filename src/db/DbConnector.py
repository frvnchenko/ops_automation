# Подключение к бд
import os
import psycopg2
import yaml
from pathlib import Path


class DbConnector:
    def __init__(self, config_path=None):
        src_dir = Path(__file__).parent.parent  # Путь до src
        print("src_dir: ", src_dir)

        config_path = src_dir.parent / "config" / "db_config.yaml"  # Путь до файла

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

        self.config = self._load_config(config_path)
        self.connection = None

    def _load_config(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def connect(self) -> None:
        """Устанавливает соединение с PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.config["database"]["host"],
                user=self.config["database"]["user"],
                password=self.config["database"]["password"],
                database=self.config["database"]["database"],
            )
        except psycopg2.Error as e:
            raise ConnectionError(f"Ошибка при подключении к базе данных: {e}")

    def disconnect(self) -> None:
        """Закрывает соединение с PostgreSQL"""
        if self.connection:
            self.connection.close()
            self.connection = None  # Обнуляю ссылку, чтобы избежать повторного закрытия

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
