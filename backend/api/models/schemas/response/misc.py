from typing import List, Union

from pydantic import Field

from api.models.schemas.response import BaseResponseSchema


class HealthResponseSchema(BaseResponseSchema):
    APP_NAME: str = Field(title="App Name")
    MODE: str = Field(title="App Mode")
    DEBUG: bool = Field(title="Debug Mode")


class MessageResponseSchema(BaseResponseSchema):
    loc: Union[List[str], None] = Field(default=None, title="Location")
    msg: str = Field(title="Message")
    type: Union[str, None] = Field(default=None, title="Type")
