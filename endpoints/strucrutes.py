from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table
from models.structures.direction import DirectionData
from schemas.structures.direction import DirectionSh

router = APIRouter()


@router.post("/direction")
async def post(direction: DirectionSh,
               db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, direction, DirectionData)
    return {"Successfully added": direction}

