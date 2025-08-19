from sqlalchemy.orm import Session
from careDataBase.session import SessionLocal
from careDataBase.models.api_calls import ApiCall
from datetime import datetime, timezone

class ApiCallService:
    def __init__(self):
        self.db: Session = SessionLocal()

    # 🟢 Create
    def create_api_call(
        self,
        method: str,
        token_name: str,
        status_code: int,
        is_success: bool,
        endpoint: str,
        url: str,
        duration_ms: int = None,
        user_queried: str = None,
        device_used: str = None,
        description: str = None,
        query_params: dict = None,
        response_size_bytes: int = None,
        rl_limit: int = None,
        rl_remaining: int = None,
        rl_reset_at: datetime = None,
        data_downloaded_at: datetime = None,
    ):
        api_call = ApiCall(
            method=method,
            token_name=token_name,
            status_code=status_code,
            is_success=is_success,
            endpoint=endpoint,
            url=url,
            duration_ms=duration_ms,
            user_queried=user_queried,
            device_used=device_used,
            description=description,
            query_params=query_params,
            response_size_bytes=response_size_bytes,
            rl_limit=rl_limit,
            rl_remaining=rl_remaining,
            rl_reset_at=rl_reset_at,
            data_downloaded_at=data_downloaded_at,
            timestamp=datetime.now(timezone.utc),
        )
        self.db.add(api_call)
        self.db.commit()
        self.db.refresh(api_call)
        return api_call

    # 🔵 Read one
    def get_api_call(self, call_id: int):
        return self.db.query(ApiCall).filter(ApiCall.id == call_id).first()

    # 🔵 Read all
    def get_all_api_calls(self, skip: int = 0, limit: int = 100):
        return self.db.query(ApiCall).order_by(ApiCall.timestamp.desc()).offset(skip).limit(limit).all()

    # 🟠 Update
    def update_api_call(self, call_id: int, **kwargs):
        api_call = self.get_api_call(call_id)
        if not api_call:
            return None
        for key, value in kwargs.items():
            if hasattr(api_call, key):
                setattr(api_call, key, value)
        self.db.commit()
        self.db.refresh(api_call)
        return api_call

    # 🔴 Delete
    def delete_api_call(self, call_id: int):
        api_call = self.get_api_call(call_id)
        if not api_call:
            return None
        self.db.delete(api_call)
        self.db.commit()
        return api_call


if __name__ == "__main__":
    service = ApiCallService()

    # יצירה
    call = service.create_api_call(
        method="GET",
        token_name="my_token",
        status_code=200,
        is_success=True,
        endpoint="/2/users/:id/tweets",
        url="https://api.twitter.com/2/users/123/tweets?max_results=10",
        duration_ms=120,
        response_size_bytes=2048,
        query_params={"max_results": 10}
    )
    print("✅ נוצר API call:", call.id, call.status_code)

    # שליפה
    c = service.get_api_call(call.id)
    print("📌 שליפה:", c.id, c.endpoint, c.timestamp)

    # עדכון
    updated = service.update_api_call(call.id, description="בדיקה ראשונית", duration_ms=150)
    print("✏️ עודכן:", updated.id, updated.description, updated.duration_ms)

    # שליפה של כולם
    calls = service.get_all_api_calls(limit=5)
    print("📜 כל הקריאות:", [c.id for c in calls])


