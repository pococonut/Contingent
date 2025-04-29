from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate

from api.db import endpoints as db_endpoints
from api.structure.direction import endpoints as direction_endpoints
from api.structure.department import endpoints as department_endpoints
from api.structure.fgos import endpoints as fgos_endpoints
from api.structure.group import endpoints as group_endpoints
from api.structure.profile import endpoints as profile_endpoints
from api.structure.subgroup import endpoints as subgroup_endpoints
from api.structure.structure import endpoints as structure_endpoints
from api.student_card import endpoints as student_card_endpoints
from api.students_list.number_contingent import endpoints as number_contingent_endpoints
from api.students_list.student_cards import endpoints as student_cards_endpoints
from api.authentication import endpoints as authentication_endpoints
from api.excel import endpoints as excel_endpoints
from api.user import endpoints as user_endpoints

app = FastAPI(title="Contingent")
add_pagination(app)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(direction_endpoints.router)
app.include_router(department_endpoints.router)
app.include_router(fgos_endpoints.router)
app.include_router(group_endpoints.router)
app.include_router(profile_endpoints.router)
app.include_router(subgroup_endpoints.router)
app.include_router(structure_endpoints.router)
app.include_router(number_contingent_endpoints.router)
app.include_router(student_cards_endpoints.router)
app.include_router(student_card_endpoints.router)
app.include_router(excel_endpoints.router)
app.include_router(user_endpoints.router)
app.include_router(authentication_endpoints.router)
app.include_router(db_endpoints.router)
