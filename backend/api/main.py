import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from api.config.factory import settings
from api.events.startup import store_district_data
from api.models.schemas.response.misc import HealthResponseSchema, MessageResponseSchema
from api.utils.docs import retrieve_api_metadata, retrieve_tags_metadata
from api.utils.enums import Tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.run("alembic upgrade head", shell=True)
    await store_district_data()
    yield


app = FastAPI(
    lifespan=lifespan,
    **retrieve_api_metadata(),
    openapi_tags=retrieve_tags_metadata(),
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": MessageResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": MessageResponseSchema},
        status.HTTP_403_FORBIDDEN: {"model": MessageResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": MessageResponseSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageResponseSchema},
    },
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get(
    "/health",
    response_model=HealthResponseSchema,
    summary="Health Check",
    description="Health check for the API",
    tags=[Tags.server_health],
)
async def health_check():
    return settings.model_dump()
