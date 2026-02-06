from typing import Annotated


from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from api.public.v1.request import ShortenRequest
from api.public.v1.response import ShortenResponse
from app.public.v1.service.dependency import get_shortener_service
from app.public.v1.service.shortener import ShortenerService
from core.fastapi.decorators.service import service_response_decorator

public_router = APIRouter(prefix="/v1", tags=["Shortener URL Service"])

@public_router.get(
    "/go/{code}",
    summary="Redirect to domain by shortened URL",
)
@service_response_decorator()
def redirect_by_code(
        code: str,
        shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)]
):
    """Редиректит на домен, если есть сокращенная ссылка"""
    url = shortener_service.redirect_by_short_link(code=code)
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@public_router.post(
    "/shorten",
    response_model=ShortenResponse,
    summary="Create Shorten URL",
)
@service_response_decorator()
def shorten(
    request: Request,
    body: ShortenRequest,
    shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)]
):
    """Создает короткую ссылку"""
    return shortener_service.create_short_link(body=body, base_url=request.base_url)
