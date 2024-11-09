import jwt
import bcrypt
from datetime import timedelta, datetime

from schemas.auth.authentication import UserSchema
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

TOKEN_TYPE_FILED = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(payload: dict,
               key: str = str(SECRET_KEY),
               algorithm: str = str(ALGORITHM),
               expire_minutes: int = int(ACCESS_TOKEN_EXPIRE_MINUTES),
               expire_timedelta: timedelta | None = None):
    """
    Функция предназначена для шифрования JWT на основе переданных данных
    :param payload: Полезные данные
    :param key: Секретный ключ
    :param algorithm: Алгоритм шифрования
    :param expire_minutes: Время действия токена по умолчанию
    :param expire_timedelta: Заданное время действия токена
    :return: Функция возвращает закодированный JWT
    """
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload=to_encode,
                         key=key,
                         algorithm=algorithm)
    return encoded


def decode_jwt(token: str,
               key: str = str(SECRET_KEY),
               algorithm: str = str(ALGORITHM)):
    """
    Функция предназначена для дешифрования JWT на основе переданных данных
    :param token: JWT
    :param key: Секретный ключ
    :param algorithm: Алгоритм шифрования
    :return: Декодированный JWT
    """
    decoded = jwt.decode(jwt=token,
                         key=key,
                         algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Функция предназначена для шифрования пароля пользователя
    :param password: Пароль пользователя
    :return: Зашифрованный пароль
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: bytes, hashed_password: bytes) -> bool:
    """
    Функция предназначена для валидации пароля переданного
    пользователем и зашифрованным паролем пользователя
    :param password: Пароль пользователя
    :param hashed_password: Зашифрованный пароль пользователя
    :return: Булево значение: True - пароли совпали, иначе False
    """
    return bcrypt.checkpw(password=password, hashed_password=hashed_password)


def create_jwt(token_type: str,
               token_data: dict,
               expire_minutes: int = int(ACCESS_TOKEN_EXPIRE_MINUTES),
               expire_timedelta: timedelta | None = None) -> str:
    """
    Функция предназначена для шифрования JWT на основе переданных данных
    :param token_type: Тип токена
    :param token_data: Полезные данные токена
    :param expire_minutes: Время действия токена по умолчанию
    :param expire_timedelta: Заданное время действия токена
    :return:
    """
    jwt_payload = {TOKEN_TYPE_FILED: token_type}
    jwt_payload.update(token_data)

    return encode_jwt(payload=jwt_payload,
                      expire_minutes=expire_minutes,
                      expire_timedelta=expire_timedelta)


def create_access_token(user: UserSchema) -> str:
    """
    Функция предназначена для м=создания ACCESS токена
    :param user: Данные пользователя
    :return: ACCESS токен
    """
    jwt_payload = {"sub": user.username,
                   "username": user.username,
                   "email": user.email}

    return create_jwt(token_type=ACCESS_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user: UserSchema):
    """
    Функция предназначена для создания REFRESH токена
    :param user: Данные пользователя
    :return: REFRESH токен
    """
    jwt_payload = {"sub": user.username}

    return create_jwt(token_type=REFRESH_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_timedelta=timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS)))

