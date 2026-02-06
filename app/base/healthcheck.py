from sqlite3 import Connection
from dataclasses import dataclass
from logging import getLogger
from typing import Tuple


logger = getLogger(__name__)


@dataclass
class HealthCheckService:
    _session: Connection

    """
    Сервис healthcheck проверяет статус инфрастуктурных модулей Postgresql/Redis
    """

    def is_application_healthy(self) -> Tuple[bool, list]:
        unavailable_modules = []
        if not self._is_db_healthy():
            unavailable_modules.append("DB")
        is_ok_flag = True if not unavailable_modules else False
        return is_ok_flag, unavailable_modules

    def _is_db_healthy(self):
        try:
            self._session.execute("SELECT 1")
            return True
        except Exception as exc:
            logger.error(f"Database is unhealthy: {exc}")
            return False
