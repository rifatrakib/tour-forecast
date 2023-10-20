from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config.factory import settings
from api.events.startup import store_district_data
from api.models.schemas.response.misc import HealthResponseSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await store_district_data()
    yield


app = FastAPI(lifespan=lifespan)


@app.get(
    "/health",
    response_model=HealthResponseSchema,
    summary="Health Check",
    description="Health check for the API",
)
async def health_check():
    return settings.model_dump()
