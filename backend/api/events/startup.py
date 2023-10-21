from typing import List

import httpx

from api.models.schemas.internals.districts import DistrictsDownload


async def download_districts() -> List[DistrictsDownload]:
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return DistrictsDownload.model_validate(response.json())


async def store_district_data():
    data: DistrictsDownload = await download_districts()
    print(data)
