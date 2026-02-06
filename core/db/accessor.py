import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

from core.config import config


def get_connection():
    """Доступ по имени колонок"""

    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    # TODO: Отстой( Соединение создаётся внутри каждого вызова sqlite нельзя использовать из другого потока.

    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_db_session() -> Generator[sqlite3.Connection, None, None]:
    """Генератор для FastAPI Depends(): отдаёт сессию и закрывает после запроса."""
    with get_db() as conn:
        yield conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS short_links (
                code TEXT PRIMARY KEY,
                long_url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
