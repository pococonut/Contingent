from fastapi import APIRouter, Depends

from validation.auth_parameters import get_current_active_auth_user
from db.db_commands import create_db

router = APIRouter()


@router.get("/create_db",
            tags=["database"],
            response_description="Сообщение об успешном создании БД")
async def create_db(db=Depends(create_db),
                    token: str = Depends(get_current_active_auth_user)):
    """
    Используется для создания БД
    """
    return {"result": "database was created"}