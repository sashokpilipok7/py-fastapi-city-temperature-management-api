from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()

@router.get("/temperatures", response_model=None)
async def get_temps_list_by_city_id(city_id: int | None, db: AsyncSession = Depends(get_db)):
    if city_id:
        return await crud.get_temperatures_by_city_id(city_id=city_id, db=db)
    return await crud.get_all_temperatures(db=db)

@router.put("/temperatures/update", response_model=int)
async def update_temperature(temperature: schemas.TemperatureUpdate, db: AsyncSession = Depends(get_db)):
    result =  await crud.update_temperatures(db=db, temperature=temperature)

    if not result:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return result