from fastapi import Depends, APIRouter

from auth import helpers
from validation.auth_parameters import get_current_active_auth_user, get_current_auth_user_for_refresh, validate_auth_user
from schemas.auth.authentication import UserSchema, TokenInfo


router = APIRouter()


@router.post("/login", tags=['auth'], response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    access_token = helpers.create_access_token(user)
    refresh_token = helpers.create_refresh_token(user)

    return TokenInfo(access_token=access_token,
                     refresh_token=refresh_token)


@router.post("/refresh", tags=['auth'], response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = helpers.create_access_token(user)

    return TokenInfo(access_token=access_token)


@router.get("/check_valid_token", tags=['auth'])
def check_valid_token(user: UserSchema = Depends(get_current_active_auth_user)):

    return {"username": user.username,
            "email": user.email}

