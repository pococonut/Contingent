from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


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
