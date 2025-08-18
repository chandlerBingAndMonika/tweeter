from typing import TypedDict, Any, Optional


class ApiCallResult(TypedDict):
    success: bool                # האם הבקשה הצליחה
    status_code: int             # קוד ה־HTTP שחזר מטוויטר
    error_message: Optional[str] # במקרה של שגיאה
    rate_limit: Optional[dict]   # נתוני רייט לימיט (limit, remaining, reset)
    json_data: Optional[Any]     # ה־JSON הגולמי מה־API
    elapsed_time: float          # כמה שניות עברו מהקריאה ועד קבלת התשובה
