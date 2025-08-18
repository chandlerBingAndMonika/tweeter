# types_policy.py
from dataclasses import dataclass
from typing import Optional, List, Literal
from datetime import datetime

# --- סיווג שגיאה בסיסי אחרי ApiCallResult ---
ErrorKind = Literal[
    "rate_limit",        # 429 או לפי headers
    "user_restricted",   # 401/403/forbidden על יוזר מוגן/מוגבל
    "network",           # timeout/connection
    "server_5xx",        # 500-599
    "bad_request_4xx",   # 400/404 וכו' (לא רלוונטי לרה-טריי)
    "unknown"
]

# --- פעולה מומלצת לשלב הבא ---
NextAction = Literal[
    "retry_now",             # לנסות שוב מיידית (עם טוקן אחר אם יש)
    "retry_after_reset",     # לחכות עד reset (רייט-לימיט)
    "retry_with_backoff",    # רה-טריי אחרי השהיה קצובה (רשת/5xx)
    "skip_user",             # לדלג על המשתמש (מוגבל/לא נגיש)
    "abort_task",            # לוותר על המשימה הזו
    "proceed"                # הצליח – להמשיך בעיבוד/שמירה
]

@dataclass(frozen=True)
class RetryPlan:
    action: NextAction
    wait_seconds: Optional[int] = None      # backoff כללי (למשל 60)
    wait_until: Optional[datetime] = None   # זמן reset מרייט-לימיט, אם ידוע
    use_other_token: bool = False           # האם לנסות טוקן אחר עכשיו
    note: Optional[str] = None              # הערת דיבוג קצרה

# --- החלטה אחרי ApiCallResult: מה לעשות הלאה ---
@dataclass(frozen=True)
class ApiDecision:
    ok: bool                    # True אם ההורדה הצליחה ואפשר להתקדם
    error_kind: Optional[ErrorKind] = None
    retry: Optional[RetryPlan] = None

# -------------------------------------------------------------------
# קבלת מספר הציוצים של יוזר → תכנון מה להוריד
# -------------------------------------------------------------------

# איך לפעול אחרי שקיבלנו את ספירת הציוצים (total)
CountMode = Literal[
    "fetch_all_history",   # להוריד את כל ההיסטוריה (נפרוס לפרוסות של 50)
    "fetch_more_partial"   # להוריד רק המשך/כמות מסוימת לפי בקשה
]

@dataclass(frozen=True)
class FetchSlice:
    """
    פרוסה אחת של הורדה: עד 50 ציוצים.
    משתמשים ב-until_id כדי ללכת אחורה בזמן.
    """
    until_id: Optional[str]   # אם None נתחיל מהטוויט הכי חדש; אחרת נלך אחורה מה-id הזה
    max_results: int = 50

@dataclass(frozen=True)
class FetchPlan:
    """
    תכנית הורדה מורכבת מפרוסות של 50 ציוצים כל פעם.
    מספר הפרוסות נגזר ממה שרוצים להוריד.
    """
    user_id: str
    mode: CountMode
    total_count: int                   # כמה ציוצים יש (לפי API)
    already_downloaded: int = 0        # כמה כבר יש אצלנו (אם ידוע)
    target_additional: Optional[int] = None  # אם מבקשים רק המשך חלקי (N)
    slices: List[FetchSlice] = None     # ימולא לפני הרצה (רשימת פרוסות)

# דוגמה כללית לשימוש (לוגיקה חיצונית תחשב את slices):
# - fetch_all_history: נחשב כמה פרוסות של 50 צריך כדי לכסות את (total_count - already_downloaded)
# - fetch_more_partial: נחשב כמה פרוסות כדי לכסות target_additional
