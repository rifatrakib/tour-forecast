from fastapi import FastAPI

from api.config.factory import settings
from api.models.schemas.response.misc import HealthResponseSchema

app = FastAPI()


@app.get(
    "/health",
    response_model=HealthResponseSchema,
    summary="Health Check",
    description="Health check for the API",
)
async def health_check():
    return settings.model_dump()
