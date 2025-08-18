# types_task.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """
    משימה להורדת 50 ציוצים אחורה מציוץ מסוים.
    - user_id מזהה את המשתמש שממנו נמשוך.
    - start_from_id הוא הציוץ שממנו נתחיל (נמשוך אחורה ממנו).
    - track_after: אם True, נוסיף את המשתמש לרשימת המעקב.
    - assigned_token: שם הטוקן (ENV key) שמשמש למשימה.
    - completed_count: כמה ציוצים הורדו בפועל.
    """
    user_id: str
    start_from_id: str
    track_after: bool = False
    assigned_token: Optional[str] = None
    completed_count: int = 0
    status: str = "pending"  # pending | running | done | failed
