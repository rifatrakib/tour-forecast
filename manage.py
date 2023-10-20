import subprocess
from enum import Enum
from typing import Union

from typer import Typer

app = Typer()


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

        subprocess.run("docker compose up --build")
    except KeyError:
        print("Invalid mode")


@app.command()
def terminate():
    subprocess.run("docker compose down")
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)


if __name__ == "__main__":
    app()
