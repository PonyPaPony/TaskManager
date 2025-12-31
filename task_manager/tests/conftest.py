import pytest
import sqlite3
import task_manager.storage_sqlite as storage

@pytest.fixture()
def db():
    conn = sqlite3.connect(":memory:")  # всегда новое подключение в тестах
    conn.row_factory = sqlite3.Row  # Создаем линии как в мейн файле

    storage.DB_CONNECTION = conn  # Присваиваем значение

    yield conn  # Гарантируем что все удалится после тестов

    conn.close()  # Выключаемся
    storage.DB_CONNECTION = None  # Возвращаем значение к исходному