from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import authentication, students_lists, excel_operations, student_card, table, structures
from api.structure.direction import endpoints as direction_endpoints
from api.structure.department import endpoints as department_endpoints
from api.structure.fgos import endpoints as fgos_endpoints
from api.structure.group import endpoints as group_endpoints
from api.structure.profile import endpoints as profile_endpoints
from api.structure.subgroup import endpoints as subgroup_endpoints
from api.structure.structure import endpoints as structure_endpoints

app = FastAPI(title="Contingent")

origins = [
    "http://localhost:5173",
]

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


app.include_router(authentication.router)
app.include_router(students_lists.router)
app.include_router(student_card.router)
app.include_router(excel_operations.router)
app.include_router(table.router)


