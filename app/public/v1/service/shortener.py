import secrets
import string
from dataclasses import dataclass

from starlette.datastructures import URL

from api.public.v1.request import ShortenRequest
from api.public.v1.response import ShortenResponseSchema
from core.exceptions.service import ServiceAPIException, ServiceAPIResponseStatus
from repositories.shortener import ShortenerRepository


@dataclass
class ShortenerService:
    shortener_repo: ShortenerRepository

    def create_short_link(self, base_url: URL, body: ShortenRequest) -> ShortenResponseSchema:
        long_url = str(body.url)
        short_url = str(base_url).rstrip("/") # для тестов
        code = self.shortener_repo.get_code_by_long_url(long_url=long_url)
        if code:
            return ShortenResponseSchema(short_code=code, short_url=f"{short_url}/api/public/v1/go/{code}")
        code = self._generate_short_code()
        self.shortener_repo.create_short_link(long_url=long_url, code=code)
        return ShortenResponseSchema(short_code=code, short_url=f"{short_url}/api/public/v1/go/{code}")

    def redirect_by_short_link(self, code: str) -> str | None:
        long_url = self.shortener_repo.get_by_code(code=code)
        if not long_url:
            raise ServiceAPIException(
                status=ServiceAPIResponseStatus.NOT_FOUND_DATA,
                message=f"Could not find short code {code}",
                extra_data={"code": code},
            )
        return long_url

    @staticmethod
    def _generate_short_code(length: int = 6) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))