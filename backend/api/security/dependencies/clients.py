from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.config.factory import settings


def get_async_database_session() -> AsyncSession:
    engine = create_async_engine(settings.RDS_URI)
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return SessionLocal()
