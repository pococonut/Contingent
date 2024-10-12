from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import authentication, students_lists, import_excel, student_card, table


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
app.include_router(import_excel.router)
app.include_router(student_card.router)
app.include_router(table.router)


