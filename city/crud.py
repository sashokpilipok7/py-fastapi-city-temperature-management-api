from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) ->  list[models.City]:
    cities = await db.scalars(select(models.City))

    return cities.all()