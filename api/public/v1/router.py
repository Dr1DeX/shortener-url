from typing import Annotated


from fastapi import APIRouter, Depends

from app.public.v1.service.dependency import get_shortener_service
from app.public.v1.service.shortener import ShortenerService
from core.fastapi.decorators.service import service_response_decorator

public_router = APIRouter(prefix="/v1", tags=["Shortener URL Service"])

@public_router.get(
    "/go/{code}",
)
@service_response_decorator()
def redirect_by_code(
        code: str,
        shortener_service: Annotated[ShortenerService, Depends(get_shortener_service)]
):
    return shortener_service.redirect_by_short_link(code=code)