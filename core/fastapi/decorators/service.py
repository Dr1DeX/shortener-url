from functools import wraps
from logging import getLogger
from traceback import print_exc

from fastapi.responses import ORJSONResponse
from starlette.responses import Response

from api.base.v1.response import BaseResponseModel
from core.exceptions.service import ServiceAPIResponseStatus, ServiceAPIException

logger = getLogger(__name__)


def service_response_decorator(status_response: int = 200):
    """
    дефолтный респонс декоратор используется в public рутах
    """

    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            try:
                response = handler(*args, **kwargs)
                if isinstance(response, Response):
                    return response
                return BaseResponseModel(result=response, status=status_response)

            except ServiceAPIException as err:
                response_body = BaseResponseModel(
                    result=err.extra_data,
                    error_message=err.message,
                    status=err.status,
                )
                return ORJSONResponse(
                    content=response_body.model_dump(),
                    status_code=err.status,
                )

            except Exception as err:
                # да я злодей)

                print_exc()
                response_body = BaseResponseModel(
                    result={},
                    error_message=str(err),
                    status=ServiceAPIResponseStatus.GENERAL_ERROR,
                )
                return ORJSONResponse(
                    content=response_body.dict(),
                    status_code=ServiceAPIResponseStatus.GENERAL_ERROR,
                )

        return wrapper

    return decorator
