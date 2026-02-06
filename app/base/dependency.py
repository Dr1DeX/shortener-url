from fastapi import Depends
from sqlite3 import Connection

from app.base.healthcheck import HealthCheckService
from core.db.accessor import get_db_session


def get_healthcheck_service(
    session: Connection = Depends(get_db_session),
) -> HealthCheckService:
    return HealthCheckService(_session=session)
