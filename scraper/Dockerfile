FROM python:3.9-slim-buster

WORKDIR /scraper

COPY requirements.txt /scraper/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /scraper/requirements.txt
COPY ./forecast /scraper/forecast
COPY ./main.py /scraper/main.py
COPY ./scrapy.cfg /scraper/scrapy.cfg

CMD ["python", "main.py"]
