from pydantic import ConfigDict

from api.models.schemas import BaseSchema


class BaseRequestSchema(BaseSchema):
    model_config = ConfigDict(extra="forbid")
