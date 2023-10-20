from typing import List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.districts.repository import create_districts, read_districts
from api.models.schemas.internals.districts import DistrictsDownload
from api.security.dependencies.clients import get_async_database_session


async def download_districts() -> List[DistrictsDownload]:
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return DistrictsDownload.model_validate(response.json())


async def store_district_data():
    session: AsyncSession = get_async_database_session()

    if await read_districts(session):
        print("Districts already exist in the database.")
        await session.close()
        return

    data: DistrictsDownload = await download_districts()
    await create_districts(session, data)
    await session.close()
