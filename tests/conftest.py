import pytest
from pathlib import Path

from fastapi.testclient import TestClient

from core.db.accessor import init_db
from api.public.v1.app import public_subapi

@pytest.fixture(scope="function")
def test_db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Подменяем путь к БД на временный файл для изоляции тестов"""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("core.config.config.DB_PATH", str(db_path))
    return db_path


@pytest.fixture
def client(test_db_path: Path):
    """Клиент для публичного API (субприложение /api/public)."""

    init_db()
    with TestClient(public_subapi) as c:
        yield c
