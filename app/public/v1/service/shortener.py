import secrets
import string
from dataclasses import dataclass

from repositories.shortener import ShortenerRepository


@dataclass
class ShortenerService:
    shortener_repo: ShortenerRepository

    def create_short_link(self, long_url: str) -> str:
        code = self._generate_short_code()
        self.shortener_repo.create_short_link(long_url=long_url, code=code)
        return code

    def redirect_by_short_link(self, code: str) -> str | None:
        return self.shortener_repo.get_by_code(code=code)

    @staticmethod
    def _generate_short_code(length: int = 6) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))