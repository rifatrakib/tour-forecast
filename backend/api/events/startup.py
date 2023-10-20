import json

import httpx


async def download_districts():
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.json()


async def store_district_data():
    data = await download_districts()
    with open("bd-districts.json", "w") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
