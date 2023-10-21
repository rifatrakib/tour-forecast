import subprocess
from enum import Enum
from typing import Union

from pydantic import BaseModel
from typer import Typer

app = Typer()


class InfluxDBConfig(BaseModel):
    INFLUXDB_HOST: str
    INFLUXDB_PORT: int
    INFLUXDB_USER: str
    INFLUXDB_PASSWORD: str
    INFLUXDB_ORG: str


class ScraperConfig(BaseModel):
    REDIS_HOST: str
    REDIS_PORT: int
    INFLUXDB_HOST: str
    INFLUXDB_PORT: int
    INFLUXDB_ORG: str


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"


@app.command()
def deploy(mode: Union[str, None] = "development"):
    try:
        if mode not in Modes.__members__.values():
            raise KeyError

        with open("backend/.env", "w") as writer:
            writer.write(f"MODE={mode}\n")

        with open(f"backend/secrets/{mode}.json") as reader:
            secrets = reader.read()

        influxdb_secrets = InfluxDBConfig.model_validate_json(secrets)
        scraper_secrets = ScraperConfig.model_validate_json(secrets)

        with open("backend/.env.influxdb", "w") as writer:
            for key, value in influxdb_secrets.model_dump().items():
                writer.write(f"{key}={value}\n")

        with open("scraper/.env", "w") as writer:
            for key, value in scraper_secrets.model_dump().items():
                writer.write(f"{key}={value}\n")

        subprocess.run("docker compose up --build")
    except KeyError:
        print("Invalid mode")


@app.command()
def terminate():
    subprocess.run("docker compose down")
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)


if __name__ == "__main__":
    app()
