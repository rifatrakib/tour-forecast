from pathlib import Path

import aioredis
from aioredis.client import Redis
from fastapi import Depends, HTTPException, status
from influxdb_client import InfluxDBClient

from api.config.factory import settings
from api.database.cache.repository import cache_read, cache_write


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        yield redis
    finally:
        await redis.close()


async def get_influxdb_client(redis: Redis = Depends(get_redis_client)):
    token = await cache_read(redis, "influxdb-admin-token")

    if not token:
        file = Path("secrets/influxdb-admin-token.txt")

        if file.exists():
            with open(file) as reader:
                token = reader.read()
            await cache_write(redis, "influxdb-admin-token", token, ttl=None)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="InfluxDB admin token not found.",
            )

    try:
        client: InfluxDBClient = InfluxDBClient(
            url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
            token=token,
            org=settings.INFLUXDB_ORG,
        )
        yield client
    finally:
        client.close()
