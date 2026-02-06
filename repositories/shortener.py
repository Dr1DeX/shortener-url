from dataclasses import dataclass

from sqlite3 import Connection


@dataclass
class ShortenerRepository:
    _session: Connection

    def create_short_link(self, long_url: str, code: str) -> str:
        self._session.execute(
            "INSERT INTO short_links (code, long_url) VALUES (?, ?)",
            (code, long_url),
        )
        return code

    def get_by_code(self, code: str) -> str | None:
        row = self._session.execute(
            "SELECT long_url FROM short_links WHERE code = ?", (code,)
        ).fetchone()
        return row["long_url"] if row else None