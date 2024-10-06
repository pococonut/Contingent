from schemas.authentication import UserSchema
from auth.helpers import hash_pasword


polina = UserSchema(
    username="po",
    password=hash_pasword("po"),
    email='po@mail.ru'
)

serafim = UserSchema(
    username="serafim",
    password=hash_pasword("123"),
    email="serafim@gmail.com"
)

users_db: dict[str, UserSchema] = {
    polina.username: polina,
    serafim.username: serafim,
}