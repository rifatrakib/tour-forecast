from typing import List

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from api.config.factory import settings
from api.models.schemas.internals.forecasts import Forecast


def create_forecast_points(client: InfluxDBClient, forecasts: List[Forecast]):
    points = []
    for forecast in forecasts:
        points.append(
            Point("temperature")
            .tag("district", forecast.name)
            .field("id", forecast.id)
            .field("division_id", forecast.division_id)
            .field("bn_name", forecast.bn_name)
            .field("lat", forecast.lat)
            .field("long", forecast.long)
            .field("temperature", forecast.temperature)
            .time(forecast.time)
        )

    with client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=settings.INFLUXDB_BUCKET, record=points)
