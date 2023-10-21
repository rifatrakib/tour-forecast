from aioredis.client import Redis


async def cache_write(client: Redis, key: str, data: str) -> None:
    await client.set(key, data, ex=300)


async def cache_read(client: Redis, key: str) -> str:
    return await client.get(key)
