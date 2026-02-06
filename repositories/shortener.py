from dataclasses import dataclass

from core.db.accessor import get_db


@dataclass
class ShortenerRepository:
    def get_code_by_long_url(self, long_url: str) -> str | None:
        """Возвращает существующий code для long_url, если есть."""
        with get_db() as conn:
            row = conn.execute(
                "SELECT code FROM short_links WHERE long_url = ? ORDER BY created_at LIMIT 1",
                (long_url,),
            ).fetchone()
        return row["code"] if row else None

    def create_short_link(self, long_url: str, code: str) -> str:
        """Создает ссылку для редиректа"""
        with get_db() as conn:
            conn.execute(
                "INSERT INTO short_links (code, long_url) VALUES (?, ?)",
                (code, long_url),
            )
        return code

    def get_by_code(self, code: str) -> str | None:
        """Получить длинную ссылку"""
        with get_db() as conn:
            row = conn.execute(
                "SELECT long_url FROM short_links WHERE code = ?", (code,)
            ).fetchone()
        return row["long_url"] if row else None