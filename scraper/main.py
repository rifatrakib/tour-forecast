import subprocess
import time
from datetime import datetime, timedelta

from redis import Redis

from forecast import settings


def run_scraper():
    while True:
        client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        token = client.get("influxdb-admin-token")

        if token:
            client.close()
            break

        print("Waiting for influxdb-admin-token")
        time.sleep(10)

    while True:
        current_time = datetime.now().replace(microsecond=0, second=0, minute=0)
        next_run = current_time + timedelta(hours=1)
        print(f"Running scraper at {current_time}")
        subprocess.run("scrapy crawl meteo", shell=True)
        print(f"Next run at {next_run}")
        time.sleep((next_run - datetime.now()).seconds + 1)


if __name__ == "__main__":
    run_scraper()
