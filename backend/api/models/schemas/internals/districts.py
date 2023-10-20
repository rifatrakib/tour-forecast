from pydantic import Field

from api.models.schemas import BaseSchema


class District(BaseSchema):
    id: int = Field(title="District ID")
    division_id: int = Field(title="Division ID")
    name: str = Field(title="District Name")
    bn_name: str = Field(title="District Name in Bangla")
    lat: float = Field(title="Latitude")
    long: float = Field(title="Longitude")


class DistrictsDownload(BaseSchema):
    districts: list[District] = Field(default_factory=list, title="Districts")
