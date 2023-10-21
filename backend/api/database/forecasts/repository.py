from datetime import date, timedelta
from typing import Any, Dict, List

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from api.config.factory import settings
from api.database.forecasts.utils import judge_plan_feasibility, process_coolest_districts_data
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


def read_coolest_districts(client: InfluxDBClient) -> List[Dict[str, Any]]:
    query = (
        'import "date"'
        f'from(bucket: "{settings.INFLUXDB_BUCKET}")'
        f"|> range(start: {date.today()}, stop: 7d)"
        '|> filter(fn: (r) => r["_measurement"] == "temperature" and r["_field"] == "temperature")'
        '|> filter(fn: (r) => date.hour(t: r["_time"]) == 14)'
        '|> group(columns: ["district"])'
        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
    )

    with client:
        query_api = client.query_api()
        result = query_api.query_data_frame(query=query, org=settings.INFLUXDB_ORG)

    return process_coolest_districts_data(result)


def determine_plan_feasibility(
    client: InfluxDBClient,
    start: str,
    destination: str,
    time: date,
) -> bool:
    query = (
        'import "date"'
        f'from(bucket: "{settings.INFLUXDB_BUCKET}")'
        f"|> range(start: {time}, stop: {time + timedelta(days=1)})"
        '|> filter(fn: (r) => r["_measurement"] == "temperature" and r["_field"] == "temperature")'
        f'|> filter(fn: (r) => r["district"] == "{start}" or r["district"] == "{destination}")'
        '|> filter(fn: (r) => date.hour(t: r["_time"]) == 14)'
        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
    )

    with client:
        query_api = client.query_api()
        result = query_api.query_data_frame(query=query, org=settings.INFLUXDB_ORG)

    return judge_plan_feasibility(result, start, destination)
