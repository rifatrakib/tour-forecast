from pathlib import Path

import aioredis
import httpx

from api.config.factory import settings
from api.database.cache.repository import cache_read, cache_write


async def influxdb_onboarding():
    file = Path("secrets/influxdb-admin-token.txt")
    redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
    token = await cache_read(redis, "influxdb-admin-token")

    if token:
        print("InfluxDB admin token already exists. Skipping onboarding.")
        return
    else:
        if file.exists():
            with open(file, "r") as f:
                token = f.read()

            if token:
                await cache_write(redis, "influxdb-admin-token", token, ttl=None)
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

    with open(file, "w") as f:
        f.write(data["auth"]["token"])
