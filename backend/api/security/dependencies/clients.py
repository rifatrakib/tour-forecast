import aioredis
from aioredis.client import Redis
from fastapi import Depends
from influxdb_client import InfluxDBClient

from api.config.factory import settings
from api.database.cache.repository import cache_read


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        yield redis
    finally:
        await redis.close()


async def get_influxdb_client(redis: Redis = Depends(get_redis_client)):
    token = await cache_read(redis, "influxdb-admin-token")

    try:
        client: InfluxDBClient = InfluxDBClient(
            url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
            token=token,
            org=settings.INFLUXDB_ORG,
        )
        yield client
    finally:
        client.close()
