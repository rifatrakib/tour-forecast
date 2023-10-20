from fastapi import FastAPI

from api.config.factory import settings

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"app_name": settings.APP_NAME, "mode": settings.MODE}
