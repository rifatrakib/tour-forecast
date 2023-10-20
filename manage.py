import subprocess

from typer import Typer

app = Typer()


@app.command()
def deploy():
    subprocess.run("docker compose up --build")


@app.command()
def terminate():
    subprocess.run("docker compose down")
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)


if __name__ == "__main__":
    app()
