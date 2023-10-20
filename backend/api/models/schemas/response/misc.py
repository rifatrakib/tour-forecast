from typing import List, Union

from api.models.schemas.response import BaseResponseSchema


class HealthResponseSchema(BaseResponseSchema):
    APP_NAME: str
    MODE: str
    DEBUG: bool


class MessageResponseSchema(BaseResponseSchema):
    loc: Union[List[str], None] = None
    msg: str
    type: Union[str, None] = None
