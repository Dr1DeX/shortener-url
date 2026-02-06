from fastapi import Depends
from sqlite3 import Connection

from repositories.shortener import ShortenerRepository
from core.db.accessor import get_db_session


def get_shortener_repository(
    session: Connection = Depends(get_db_session),
) -> ShortenerRepository:
    return ShortenerRepository(_session=session)
