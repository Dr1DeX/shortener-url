from dataclasses import dataclass

from core.db.accessor import get_db


@dataclass
class ShortenerRepository:
    def create_short_link(self, long_url: str, code: str) -> str:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO short_links (code, long_url) VALUES (?, ?)",
                (code, long_url),
            )
        return code

    def get_by_code(self, code: str) -> str | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT long_url FROM short_links WHERE code = ?", (code,)
            ).fetchone()
        return row["long_url"] if row else None