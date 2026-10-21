from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) ->  list[models.DBTemperature]:
    temperatures = await db.scalars(select(models.DBTemperature))

    return temperatures.all()

async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) ->  models.DBTemperature:
    temperature = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.city_id == city_id))

    return temperature.all()

async def update_temperatures(db: AsyncSession, city: schemas.TemperatureUpdate) -> models.DBTemperature:
    db_city = models.DBTemperature(name=city.name)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city