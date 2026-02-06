from fastapi import FastAPI

from api.base.v1.response.base import BaseResponseModel
from api.public.v1.router import public_router
from core.exceptions.service import ServiceAPIException
from core.fastapi.exceptions.handlers import service_api_exception_handler


public_subapi = FastAPI()

public_subapi.include_router(
    public_router,
    responses={
        "default": {
            "model": BaseResponseModel,
        },
    },
)

public_subapi.add_exception_handler(ServiceAPIException, service_api_exception_handler)
