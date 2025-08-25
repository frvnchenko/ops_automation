import pytest
from src.db.DbConnector import DbConnector


@pytest.fixture(scope="module")
def db_connect():
    db = DbConnector()
    yield db
    db.disconnect()


@pytest.fixture
def db_cursor(db_connect):
    cursor = db_connect.get_cursor()  # Создаем курсор
    yield cursor  # Передаем курсор в тест
    cursor.close()  # Закрывает курсор после завершения теста
