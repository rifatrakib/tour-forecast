from pydantic import Field

from api.models.schemas import BaseSchema


class District(BaseSchema):
    id: int
    division_id: int
    name: str
    bn_name: str
    lat: float
    long: float


class DistrictsDownload(BaseSchema):
    districts: list[District] = Field(default_factory=list)
