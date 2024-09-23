from pydantic import BaseModel


class UserSh(BaseModel):
    username: str
    password: str
    refresh_token: str | None = None
    access_token: str | None = None


class UserAuth(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class SystemUser(UserOut):
    password: str
