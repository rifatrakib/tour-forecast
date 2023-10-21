import aioredis
from aioredis.client import Redis
from influxdb_client import InfluxDBClient

from api.config.factory import settings


def get_influxdb_client():
    client: InfluxDBClient = InfluxDBClient(
        url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
    )

    try:
        yield client
    finally:
        client.close()


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URI, decode_responses=True)
        yield redis
    finally:
        await redis.close()
