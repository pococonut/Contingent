from fastapi import FastAPI

from endpoints import authentication, students_lists, import_cards, student_card, table


app = FastAPI(title="Contingent")

app.include_router(authentication.router)
app.include_router(students_lists.router)
app.include_router(import_cards.router)
app.include_router(student_card.router)
app.include_router(table.router)


