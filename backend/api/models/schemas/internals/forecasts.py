from datetime import datetime

from pydantic import Field

from api.models.schemas.internals.districts import District


class Forecast(District):
    time: datetime = Field(title="Time")
    temperature: float = Field(title="Temperature")
