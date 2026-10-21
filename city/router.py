from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas

router = APIRouter()

@router.get("/city", response_model=None)
async def get_city_list(db: AsyncSession = Depends(get_db)):
    return crud.get_all_cities(db=db)