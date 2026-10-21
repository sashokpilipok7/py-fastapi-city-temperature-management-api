from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()

@router.get("/temperatures", response_model=None)
async def get_temps_list(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/", response_model=None)
async def get_temps_list_by_city_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures_by_city_id(city_id=city_id, db=db)

# @router.delete("/cities/{city_id}", response_model=int)
# async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
#     result =  await crud.delete_city(db=db, city_id=city_id)
#
#     if not result:
#         raise HTTPException(status_code=404, detail="City not found")
#     return city_id