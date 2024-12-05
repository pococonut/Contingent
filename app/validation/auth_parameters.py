from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db.fake_db import users_db
from schemas.auth.authentication import UserSchema
from helpers import auth

http_bearer = HTTPBearer(auto_error=False)


def validate_auth_user(user_from_req: UserSchema):
    """
    Функция проверяет существование пользователя в БД,
    валидирует переданный пароль, проверяет статус активности
    :param user_from_req: Данные пользователя
    :return: Данные пользователя, если не возникло исключения
    """
    username = user_from_req.username
    password = user_from_req.password
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!"
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")

    return user


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    """
    Функция предназначена для декодирования полезной нагрузки токена
    и проверки статуса авторизации пользователя
    :param credentials: Учетные данные из заголовка авторизации
    :return: Полезная нагрузка токена
    """
    try:
        token = credentials.credentials
        payload = auth.decode_jwt(token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}"
        )
    return payload


def get_current_auth_user_for_refresh(payload: dict = Depends(get_current_token_payload)):
    """
    Функция предназначена для валидации REFRESH токена
    :param payload: Полезные данные токена
    :return: Данные пользователя
    """
    validate_token_type(payload, auth.REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)):
    """
    Функция предназначена для валидации ACCESS токена
    :param payload: Полезные данные токена
    :return: Данные пользователя
    """
    validate_token_type(payload, auth.ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
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
    current_token_type = payload.get(auth.TOKEN_TYPE_FILED)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    """
    Функция проверяет существование пользователя в БД
    :param payload: Полезные данные токена
    :return: Пользователь, если он присутствует в БД
    """
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid"
    )

