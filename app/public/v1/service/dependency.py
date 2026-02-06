from fastapi import Depends

from app.public.v1.service.shortener import ShortenerService
from repositories.dependency import get_shortener_repository
from repositories.shortener import ShortenerRepository


def get_shortener_service(shortener_repo: ShortenerRepository = Depends(get_shortener_repository)):
    return ShortenerService(shortener_repo=shortener_repo)