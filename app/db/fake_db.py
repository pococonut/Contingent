from schemas.auth.authentication import UserSchema
from helpers.auth import hash_password


polina = UserSchema(
    username="po",
    password=hash_password("po"),
    email='po@mail.ru'
)

serafim = UserSchema(
    username="serafim",
    password=hash_password("123"),
    email="serafim@gmail.com"
)

users_db: dict[str, UserSchema] = {
    polina.username: polina,
    serafim.username: serafim,
}