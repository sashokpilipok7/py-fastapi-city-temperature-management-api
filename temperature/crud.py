from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) ->  list[models.DBTemperature]:
    temperatures = await db.scalars(select(models.DBTemperature))

    return temperatures.all()

async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) ->  list[models.DBTemperature]:
    temperature = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.city_id == city_id))

    return temperature.all()

async def update_temperatures(db: AsyncSession, temperature: schemas.TemperatureUpdate) -> models.DBTemperature | None:
    result = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.id == temperature.id))
    db_temperature = result.first()

    if not db_temperature:
        return None

    db_temperature.date_time = temperature.date_time
    db_temperature.temperature = temperature.temperature

    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature