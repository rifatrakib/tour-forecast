import scrapy

from forecast.items import Forecast


class MeteoSpider(scrapy.Spider):
    name = "meteo"

    def start_requests(self):
        yield scrapy.Request(
            "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json",
            callback=self.parse_district_data,
        )

    def parse_district_data(self, response):
        data = response.json()
        url = "https://api.open-meteo.com/v1/forecast"

        for district in data["districts"]:
            params = {
                "latitude": district["lat"],
                "longitude": district["long"],
                "hourly": "temperature_2m",
                "timezone": "auto",
            }

            yield scrapy.Request(
                f'{url}?{"&".join([f"{k}={v}" for k, v in params.items()])}',
                callback=self.parse_district_forecast,
                cb_kwargs={
                    "id": district["id"],
                    "division_id": district["division_id"],
                    "name": district["name"],
                    "bn_name": district["bn_name"],
                    "lat": district["lat"],
                    "long": district["long"],
                },
            )

    def parse_district_forecast(self, response, **kwargs):
        data = response.json()
        data = data["hourly"]

        for ts, temperature in zip(data["time"], data["temperature_2m"]):
            yield Forecast(
                **kwargs,
                time=ts,
                temperature=temperature,
            )
