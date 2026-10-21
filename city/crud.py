from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) ->  list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()

async def create_cities(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(name=city.name)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def delete_city(db: AsyncSession, city_id: int) -> None:
    stmt = delete(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount