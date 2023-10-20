FROM python:3.9-slim-buster

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY ./api /backend/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
