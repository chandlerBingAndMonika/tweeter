# routes/tasks_router.py
from fastapi import APIRouter
from typing import List  # לא חובה אם אתה מעדיף רמזי סוג בסגנון list[...]
from my_types.input import ClientBatch
from my_types.match_task import TokenTask  # זה ה-Union המובחן עם discriminator="type"
from careTwitter.controllers.tasks_controller import TasksController

router = APIRouter(prefix="/tasks", tags=["tasks"])

def build_tasks_router(controller: TasksController) -> APIRouter:
    @router.post("/prepare", response_model=list[TokenTask])  # או: List[TokenTask]
    def prepare_tasks(batch: ClientBatch) -> list[TokenTask]:
        return controller.prepare_tasks(batch)
    return router
