from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import authentication, students_lists, excel_operations, student_card, table, structures


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

app.include_router(authentication.router)
app.include_router(students_lists.router)
app.include_router(student_card.router)
app.include_router(structures.router)
app.include_router(excel_operations.router)
app.include_router(table.router)


