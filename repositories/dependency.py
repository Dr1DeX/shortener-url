from fastapi import Depends

from repositories.shortener import ShortenerRepository


def get_shortener_repository() -> ShortenerRepository:
    return ShortenerRepository()
