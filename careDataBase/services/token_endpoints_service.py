from sqlalchemy.orm import Session
from careDataBase.session import SessionLocal
from careDataBase.models.tokens_endpoints_rl import TokensEndpointRL
from datetime import datetime

class TokensEndpointRLService:
    def __init__(self):
        self.db: Session = SessionLocal()

    # 🟢 Create
    def create_record(self, token_name: str, endpoint_bucket: str,
                      rl_limit: int = None, rl_remaining: int = None,
                      rl_reset_at=None):
        record = TokensEndpointRL(
            token_name=token_name,
            endpoint_bucket=endpoint_bucket,
            rl_limit=rl_limit,
            rl_remaining=rl_remaining,
            rl_reset_at=rl_reset_at,
            updated_at=datetime.utcnow()
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # 🔵 Read one
    def get_record(self, token_name: str, endpoint_bucket: str):
        return self.db.query(TokensEndpointRL).filter(
            TokensEndpointRL.token_name == token_name,
            TokensEndpointRL.endpoint_bucket == endpoint_bucket
        ).first()

    # 🔵 Read all
    def get_all_records(self, skip: int = 0, limit: int = 100):
        return self.db.query(TokensEndpointRL).offset(skip).limit(limit).all()

    # 🟠 Update
    def update_record(self, token_name: str, endpoint_bucket: str, **kwargs):
        record = self.get_record(token_name, endpoint_bucket)
        if not record:
            return None
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        record.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(record)
        return record

    # 🔴 Delete
    def delete_record(self, token_name: str, endpoint_bucket: str):
        record = self.get_record(token_name, endpoint_bucket)
        if not record:
            return None
        self.db.delete(record)
        self.db.commit()
        return record


if __name__ == "__main__":
    service = TokensEndpointRLService()

    # יצירה
    rec = service.create_record("my_token", "/tweets", rl_limit=300, rl_remaining=300)
    print("✅ נוצר רשומה:", rec.token_name, rec.endpoint_bucket)

    # שליפה
    r = service.get_record("my_token", "/tweets")
    print("📌 שליפה:", r.token_name, r.endpoint_bucket, r.rl_remaining)

    # עדכון
    updated = service.update_record("my_token", "/tweets", rl_remaining=250)
    print("✏️ עודכן:", updated.rl_remaining)

    # שליפת הכל
    all_recs = service.get_all_records()
    print("📜 כל הרשומות:", [(x.token_name, x.endpoint_bucket) for x in all_recs])

    # מחיקה
    deleted = service.delete_record("my_token", "/tweets")
    print("🗑️ נמחק:", deleted.token_name if deleted else "לא נמצא")
