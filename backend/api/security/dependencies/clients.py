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
