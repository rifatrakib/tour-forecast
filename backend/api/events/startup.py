from typing import Any, Dict, List

import aioredis
import httpx
from influxdb_client import InfluxDBClient

from api.config.factory import settings
from api.database.cache.repository import cache_read, cache_write
from api.database.forecasts.repository import create_forecast_points
from api.models.schemas.internals.districts import District, DistrictsDownload
from api.models.schemas.internals.forecasts import Forecast


async def download_districts() -> List[DistrictsDownload]:
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return DistrictsDownload.model_validate(response.json())


async def download_forecasts(district: District) -> List[Forecast]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": district.lat,
        "longitude": district.long,
        "hourly": "temperature_2m",
        "timezone": "auto",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    return response.json()


def process_forecast_data(district: District, data: Dict[str, Any]):
    results = []

    for ts, temperature in zip(data["time"], data["temperature_2m"]):
        results.append(
            Forecast(
                **district.model_dump(),
                time=ts,
                temperature=temperature,
            )
        )

    return results


async def store_forecast_data():
    data: DistrictsDownload = await download_districts()
    forecast_data = []

    for district in data.districts:
        response = await download_forecasts(district)
        forecast_data.extend(process_forecast_data(district, response["hourly"]))

    client: InfluxDBClient = InfluxDBClient(
        url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
    )
    create_forecast_points(client, forecast_data)


async def influxdb_onboarding():
    redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
    token = await cache_read(redis, "influxdb-admin-token")

    if token:
        print("InfluxDB admin token already exists. Skipping onboarding.")
        return

    payload = {
        "username": settings.INFLUXDB_USER,
        "password": settings.INFLUXDB_PASSWORD,
        "org": settings.INFLUXDB_ORG,
        "bucket": settings.INFLUXDB_BUCKET,
    }

    headers = {
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-platform": '"Windows"',
        "Referer": f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}/onboarding/1",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "content-type": "application/json",
    }

    url = f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}/api/v2/setup"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    data = response.json()
    await cache_write(redis, "influxdb-admin-token", data["auth"]["token"], ttl=None)
