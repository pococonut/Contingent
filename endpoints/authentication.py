import jwt
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter

from config import ALGORITHM, JWT_REFRESH_SECRET_KEY
from auth.authentication import create_access_token, verify_password, create_refresh_token
from general.dicts import fake_users_db

router = APIRouter()


@router.post('/login')
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(from_data.username, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user.password

    if not verify_password(from_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    user.refresh_token = refresh_token.decode('utf-8')

    return {"access_token": access_token,
            "refresh_token": refresh_token}


@router.get('/refresh')
async def refresh(token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")

        user = fake_users_db[username]
        user_refresh_token = user.refresh_token

        if user_refresh_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid refresh token")

        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)
        user.refresh_token = refresh_token.decode('utf-8')

        return {"access_token": access_token,
                "refresh_token": refresh_token}

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
