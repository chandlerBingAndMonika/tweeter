# main.py
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from careTwitter.routes.tasks_router import build_tasks_router
from careTwitter.controllers.tasks_controller import TasksController
from careTwitter.services.task_preparer_service import TaskPreparerService
from careTwitter.services.token_picker import RoundRobinTokenPicker
from careDataBase.session import get_db, engine   # ← חדש
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Twitter Task Preparer")

# חימום חיבור ל-DB בעלייה (אופציונלי אך מומלץ)
@app.on_event("startup")
def warmup_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

# ראוט בדיקה שה-DB נגיש
@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    return {"ok": True, "select_1": db.execute(text("SELECT 1")).scalar_one()}

# הרכבה (DI פשוט):
token_picker = RoundRobinTokenPicker()
service = TaskPreparerService(token_picker=token_picker)
controller = TasksController(service=service)
app.include_router(build_tasks_router(controller))
