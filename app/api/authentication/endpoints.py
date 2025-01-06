from fastapi import Depends, APIRouter

from api.authentication import helpers
from api.authentication.schemas import UserSchema, TokenInfo
from validation.auth_parameters import get_current_active_auth_user, get_current_auth_user_for_refresh, validate_auth_user


router = APIRouter()


@router.post("/login",
             tags=['auth'],
             response_model=TokenInfo,
             response_description="ACCESS и REFRESH токены")
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user,)):
    """
    Используется для аутентификации пользователя:
    - user: Данные пользователя
    """
    access_token = helpers.create_access_token(user)
    refresh_token = helpers.create_refresh_token(user)

    return TokenInfo(access_token=access_token,
                     refresh_token=refresh_token)


@router.post("/refresh", tags=['auth'],
             response_model=TokenInfo,
             response_model_exclude_none=True,
             response_description="Новый ACCESS токен")
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    """
    Используется для обновления ACCESS токена
    - user: Данные пользователя
    """
    access_token = helpers.create_access_token(user)

    return TokenInfo(access_token=access_token)


@router.get("/check_valid_token",
            tags=['auth'],
            response_description="Username и Email пользователя")
def check_valid_token(user: UserSchema = Depends(get_current_active_auth_user)):
    """
    Используется для проверки актуальности токена
    - user: Данные пользователя
    """
    return {"username": user.username,
            "email": user.email}

