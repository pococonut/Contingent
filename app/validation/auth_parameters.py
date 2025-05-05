from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from db.user.db_commands import get_users_from_db
from db.db_commands import get_db
from api.authentication.schemas import UserSchemaAuth
from api.authentication import helpers

http_bearer = HTTPBearer(auto_error=False)


async def validate_auth_user(user_from_req: UserSchemaAuth,
                             db: AsyncSession = Depends(get_db)):
    """
    Функция проверяет существование пользователя в БД,
    валидирует переданный пароль, проверяет статус активности
    :param db: Объект сессии
    :param user_from_req: Данные пользователя
    :return: Данные пользователя, если не возникло исключения
    """
    username = user_from_req.username
    password = user_from_req.password
    users_from_db = await get_users_from_db(db)
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!")

    if not (user := users_from_db.get(username)):
        raise unauthed_exc

    if password != users_from_db.get(username).password:  # not helpers.validate_password(password=password, hashed_password=users_from_db.get(username).password):
        print(password, users_from_db.get(username).password)
        raise unauthed_exc

    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")

    return user


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchemaAuth:
    """
    Функция предназначена для декодирования полезной нагрузки токена
    и проверки статуса авторизации пользователя
    :param credentials: Учетные данные из заголовка авторизации
    :return: Полезная нагрузка токена
    """
    try:
        token = credentials.credentials
        payload = helpers.decode_jwt(token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}"
        )
    return payload


async def get_user_by_token_sub(db, payload: dict) -> UserSchemaAuth:
    """
    Функция проверяет существование пользователя в БД
    :param db: Объект сессии
    :param payload: Полезные данные токена
    :return: Пользователь, если он присутствует в БД
    """
    username: str | None = payload.get("sub")
    users_from_db = await get_users_from_db(db)

    if user := users_from_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid"
    )


async def get_current_auth_user_for_refresh(db: AsyncSession = Depends(get_db),
                                            payload: dict = Depends(get_current_token_payload)):
    """
    Функция предназначена для валидации REFRESH токена
    :param db: Объект сессии
    :param payload: Полезные данные токена
    :return: Данные пользователя
    """
    validate_token_type(payload, helpers.REFRESH_TOKEN_TYPE)
    res = await get_user_by_token_sub(db, payload)
    return res


async def get_current_auth_user(db: AsyncSession = Depends(get_db),
                                payload: dict = Depends(get_current_token_payload)):
    """
    Функция предназначена для валидации ACCESS токена
    :param db: Объект сессии
    :param payload: Полезные данные токена
    :return: Данные пользователя
    """
    validate_token_type(payload, helpers.ACCESS_TOKEN_TYPE)
    res = await get_user_by_token_sub(db, payload)
    return res


def get_current_active_auth_user(user: UserSchemaAuth = Depends(get_current_auth_user)):
    """
    Функция предназначена для проверки статуса активности пользователя
    :param user: Данные пользователя
    :return: Данные пользователя, если не возникло исключения
    """
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )


def validate_token_type(payload: dict, token_type: str) -> bool:
    """
    Функция предназначена для валидации типа токена
    :param payload: Полезные данные токена
    :param token_type: Тип токена
    :return: True, если тип токена соответствует с переданным
    """
    current_token_type = payload.get(helpers.TOKEN_TYPE_FILED)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
    )


