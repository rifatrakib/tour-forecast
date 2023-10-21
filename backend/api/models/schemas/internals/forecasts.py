from pydantic import Field

from api.models.schemas.internals.districts import District


class Forecast(District):
    time: str = Field(title="Time")
    temperature: float = Field(title="Temperature")
