import random
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from temperature import models, schemas
from temperature.models import DBTemperature


async def get_all_temperatures(db: AsyncSession) ->  list[models.DBTemperature]:
    temperatures = await db.scalars(select(models.DBTemperature))

    return temperatures.all()

async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) ->  list[models.DBTemperature]:
    temperature = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.city_id == city_id))

    return temperature.all()



async def create_temperature_record(db: AsyncSession, temp_data: schemas.Temperature) -> DBTemperature:
    city_exists = await db.get(DBCity, temp_data.city_id)
    if not city_exists:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {temp_data.city_id} not found"
        )

    new_temperature = DBTemperature(
        city_id=temp_data.city_id,
        date_time=temp_data.date_time,
        temperature=temp_data.temperature
    )

    try:
        db.add(new_temperature)
        await db.commit()
        await db.refresh(new_temperature)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating temperature record: {e}"
        )
    return new_temperature

async def fetch_and_store_temperatures(db: AsyncSession):

    all_cities_result = await db.execute(select(DBCity))
    cities = all_cities_result.scalars().all()

    if not cities:
        return {"message": "No cities found in the database to fetch temperatures for."}

    fetched_data = []
    for city_obj in cities:
        try:
            current_temp = random.randint(1,25)


            temp_record_data = schemas.Temperature(city_id=city_obj.city_id, date_time=datetime.now(), temperature=current_temp)

            await create_temperature_record(db, temp_record_data)
            fetched_data.append(
                {"city_name": city_obj.name, "temperature": current_temp, "status": "success"}
            )
            
        except Exception as e:
            fetched_data.append(
                {"city_name": city_obj.name, "status": "failed", "error": str(e)}
            )
            print(f"Error fetching temperature for {city_obj.name}: {e}")

    return {"message": "Temperature data updated for cities.", "details": fetched_data}

# async def update_temperature(db: AsyncSession, temperature: schemas.TemperatureUpdate) -> models.DBTemperature | None:
#     result = await db.scalars(select(models.DBTemperature).where(models.DBTemperature.id == temperature.id))
#     db_temperature = result.first()
#
#     if not db_temperature:
#         return None
#
#     db_temperature.date_time = temperature.date_time
#     db_temperature.temperature = temperature.temperature
#     db_temperature.city_id = temperature.city_id
#
#     await db.commit()
#     await db.refresh(db_temperature)
#
#     return db_temperature