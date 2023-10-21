from api.models.schemas.response import BaseResponseSchema


class CoolestDistricts(BaseResponseSchema):
    district: str
    temperature: float
