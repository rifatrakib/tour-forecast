import httpx

from api.models.schemas.internals.districts import DistrictsDownload


async def download_districts():
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return DistrictsDownload.model_validate(response.json())


async def store_district_data():
    data = await download_districts()
    with open("bd-districts.json", "w") as f:
        f.write(data.model_dump_json(indent=4))
