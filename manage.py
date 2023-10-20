import subprocess
from enum import Enum
from typing import Union

from pydantic import BaseModel
from typer import Typer

app = Typer()


class PostgresConfig(BaseModel):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


class PGAdminConfig(BaseModel):
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str


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

        postgres_secrets = PostgresConfig.model_validate_json(secrets)
        pgadmin_secrets = PGAdminConfig.model_validate_json(secrets)

        with open("backend/.env.postgres", "w") as writer:
            for key, value in postgres_secrets.model_dump().items():
                writer.write(f"{key}={value}\n")

        with open("backend/.env.pgadmin", "w") as writer:
            for key, value in pgadmin_secrets.model_dump().items():
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
