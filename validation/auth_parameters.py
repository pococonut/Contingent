from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db.fake_db import users_db
from schemas.auth.authentication import UserSchema


http_bearer = HTTPBearer(auto_error=False)


def validate_auth_user(user_from_req: UserSchema):
    username = user_from_req.username
    password = user_from_req.password
    print('username = ', username)
    print('password = ', password)
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!"
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not helpers.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")

    return user


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    print('credentials = ', credentials)
    try:
        token = credentials.credentials
        payload = helpers.decode_jwt(token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}"
        )
    return payload


def get_current_auth_user_for_refresh(payload: dict = Depends(get_current_token_payload)):
    validate_token_type(payload, helpers.REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)):
    validate_token_type(payload, helpers.ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(helpers.TOKEN_TYPE_FILED)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid"
    )

