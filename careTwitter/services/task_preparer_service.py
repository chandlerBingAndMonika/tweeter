# services/task_preparer_service.py
from typing import List
from my_types.input import ClientBatch
from my_types.match_task import TokenTask, FetchTweetsTask, CountTweetsTask
from careTwitter.services.token_picker import TokenPicker

class TaskPreparerService:
    """
    ממיר קלט לקוח לרשימת משימות מצוותות לטוקן:
    - limit=None -> CountTweetsTask (נחליט אחר כך כמה להוריד)
    - limit=N    -> מפצל לפרוסות של עד 50 ציוצים (FetchTweetsTask עם seq)
    """
    def __init__(self, token_picker: TokenPicker):
        self._pick = token_picker

    def prepare(self, batch: ClientBatch) -> List[TokenTask]:
        tasks: list[TokenTask] = []
        for u in batch.users:
            user_ref = u.user_id or u.username

            if u.limit is None:
                token = self._pick(endpoint="tweets_count", user_ref=user_ref)
                tasks.append(CountTweetsTask(
                    token_name=token,
                    user_id=u.user_id,
                    username=u.username,
                ))
                continue

            # פיצול לבלוקים של עד 50
            n = int(u.limit)
            total_chunks = (n + 49) // 50
            for i in range(total_chunks):
                token = self._pick(endpoint="users_id_tweets", user_ref=user_ref)
                tasks.append(FetchTweetsTask(
                    token_name=token,
                    user_id=u.user_id,
                    username=u.username,
                    max_results=min(50, n - i*50),
                    seq=i + 1,
                ))
        return tasks
