from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import Depends, FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from influxdb_client import InfluxDBClient

from api.config.factory import settings
from api.database.forecasts.repository import determine_plan_feasibility, read_coolest_districts
from api.events.startup import influxdb_onboarding, store_forecast_data
from api.models.schemas.response.forecasts import CoolestDistricts
from api.models.schemas.response.misc import HealthResponseSchema, MessageResponseSchema
from api.security.dependencies.clients import get_influxdb_client
from api.utils.docs import retrieve_api_metadata, retrieve_tags_metadata
from api.utils.enums import Tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    await influxdb_onboarding()
    await store_forecast_data()
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


@app.get(
    "/coolest-10",
    response_model=List[CoolestDistricts],
    summary="Coolest 10 Districts",
    description="Returns the coolest 10 districts in Bangladesh in the next 7 days",
)
async def coolest_districts(client: InfluxDBClient = Depends(get_influxdb_client)):
    return read_coolest_districts(client)


@app.get(
    "/plan",
    response_model=MessageResponseSchema,
    response_model_exclude_unset=True,
    summary="Determine good or bad plan",
    description="Returns whether the plan is good or bad",
)
async def is_plan_good(
    start: str = Query(title="Start Location"),
    destination: str = Query(title="Destination Location"),
    time: date = Query(title="Date of Travel"),
    client: InfluxDBClient = Depends(get_influxdb_client),
):
    is_good = determine_plan_feasibility(client, start, destination, time)
    if is_good:
        return {"msg": "Good Plan"}
    else:
        return {"msg": "Bad Plan"}
