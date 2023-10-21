import json
from pathlib import Path
from typing import List

import httpx

from api.config.factory import settings
from api.models.schemas.internals.districts import DistrictsDownload


async def download_districts() -> List[DistrictsDownload]:
    url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return DistrictsDownload.model_validate(response.json())


async def store_district_data():
    data: DistrictsDownload = await download_districts()
    # print(data)
    return data


async def influxdb_onboarding():
    file = Path("secrets/influxdb-admin-token.json")
    if file.exists():
        with open(file) as reader:
            data = json.loads(reader.read())
            settings.INFLUXDB_TOKEN = data["token"]
            print(f"{settings = }")

        print("InfluxDB admin token already exists. Skipping onboarding.")
        return

    payload = {
        "username": settings.INFLUXDB_USER,
        "password": settings.INFLUXDB_PASSWORD,
        "org": settings.INFLUXDB_ORG,
        "bucket": f"{settings.INFLUXDB_ORG}_bucket",
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
    with open(file, "w") as writer:
        writer.write(json.dumps({"token": data["auth"]["token"]}))

    settings.INFLUXDB_TOKEN = data["auth"]["token"]
    print(f"{settings = }")
