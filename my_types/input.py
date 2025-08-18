# types_input.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class ClientUser:
    """
    פריט קלט אחד מהלקוח.
    - ציין או username או user_id (אחד מהם מספיק).
    - track_after: האם להוסיף למעקב שוטף אחרי ההורדה.
    - limit: אם None נוריד היסטוריה מלאה; אם מספר > 0 נוריד עד N ציוצים.
    """
    username: Optional[str] = None
    user_id: Optional[str] = None
    track_after: bool = False
    limit: Optional[int] = None   # None = היסטוריה מלאה, אחרת עד N

@dataclass(frozen=True)
class ClientBatch:
    """
    אוסף משתמשים כפי שמגיעים בבקשה מהלקוח.
    """
    users: List[ClientUser]
