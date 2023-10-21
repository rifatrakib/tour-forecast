from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from redis import Redis

from forecast import settings


class ForecastPipeline:
    def process_item(self, item, spider):
        redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        token = redis_client.get("influxdb-admin-token").decode("utf-8")
        redis_client.close()

        influx_client: InfluxDBClient = InfluxDBClient(
            url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
            token=token,
            org=settings.INFLUXDB_ORG,
        )

        point = (
            Point("temperature")
            .tag("district", item.name)
            .field("id", item.id)
            .field("division_id", item.division_id)
            .field("bn_name", item.bn_name)
            .field("lat", item.lat)
            .field("long", item.long)
            .field("temperature", item.temperature)
            .time(item.time)
        )

        with influx_client:
            write_api = influx_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=f"{settings.INFLUXDB_ORG}_bucket", record=point)
