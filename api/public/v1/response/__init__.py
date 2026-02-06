from pydantic import BaseModel

from api.base.v1.response import BaseResponseModel


class ShortenResponseSchema(BaseModel):
    short_code: str
    short_url: str

class ShortenResponse(BaseResponseModel):
    result: ShortenResponseSchema