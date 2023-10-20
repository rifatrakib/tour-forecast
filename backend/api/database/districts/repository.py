from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.database.districts import District
from api.models.schemas.internals.districts import DistrictsDownload


async def read_districts(session: AsyncSession) -> List[District]:
    stmt = select(District)
    query = await session.execute(stmt)
    return query.scalars().all()


async def create_districts(session: AsyncSession, data: DistrictsDownload):
    for district in data.districts:
        session.add(
            District(
                id=district.id,
                division_id=district.division_id,
                name=district.name,
                bn_name=district.bn_name,
                lat=district.lat,
                long=district.long,
            )
        )

    await session.commit()
