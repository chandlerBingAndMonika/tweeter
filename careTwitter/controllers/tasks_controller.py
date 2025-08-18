# controllers/tasks_controller.py
from typing import List
from my_types.input import ClientBatch
from my_types.match_task import TokenTask
from careTwitter.services.task_preparer_service import TaskPreparerService

class TasksController:
    """שכבת תווך דקה – יכולה להכיל ולידציות/לוגים/אודיט בהמשך"""
    def __init__(self, service: TaskPreparerService):
        self._service = service

    def prepare_tasks(self, batch: ClientBatch) -> List[TokenTask]:
        return self._service.prepare(batch)
