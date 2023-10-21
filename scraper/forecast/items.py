from datetime import datetime

from pydantic import BaseModel, Field


class Forecast(BaseModel):
    id: int = Field(title="District ID")
    division_id: int = Field(title="Division ID")
    name: str = Field(title="District Name")
    bn_name: str = Field(title="District Name in Bangla")
    lat: float = Field(title="Latitude")
    long: float = Field(title="Longitude")
    time: datetime = Field(title="Time")
    temperature: float = Field(title="Temperature")
