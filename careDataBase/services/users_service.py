from sqlalchemy.orm import Session
from careDataBase.session import SessionLocal
from careDataBase.models.users import User

class UserService:
    def __init__(self):
        self.db: Session = SessionLocal()

    # 🟢 Create
    def create_user(
        self,
        user_id: str,
        username: str,
        name: str = None,
        created_at_platform=None,
        followers_count: int = 0,
        following_count: int = 0,
        tweet_count: int = 0,
        listed_count: int = 0,
        raw_json: dict = None,
        updated_at=None
    ):
        user = User(
            user_id=user_id,
            username=username,
            name=name,
            created_at_platform=created_at_platform,
            followers_count=followers_count,
            following_count=following_count,
            tweet_count=tweet_count,
            listed_count=listed_count,
            raw_json=raw_json or {},
            updated_at=updated_at
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # 🔵 Read one
    def get_user(self, user_id: str):
        return self.db.query(User).filter(User.user_id == user_id).first()

    # 🔵 Read all
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    # 🟠 Update
    def update_user(self, user_id: str, **kwargs):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    # 🔴 Delete
    def delete_user(self, user_id: str):
        user = self.get_user(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
if __name__ == "__main__":
    service = UserService()

    # יצירת יוזר
    user = service.create_user(
        user_id="12345",
        username="test_user",
        name="Test User",
        followers_count=100,
        following_count=50,
        tweet_count=10,
        listed_count=2,
        raw_json={"id": "12345", "username": "test_user"}
    )
    print("✅ נוצר יוזר:", user.username)

    # שליפה
    u = service.get_user("12345")
    print("📌 שליפה:", u.user_id, u.username, u.followers_count)

    # עדכון
    updated = service.update_user("12345", followers_count=200, name="Updated Name")
    print("✏️ עודכן:", updated.name, updated.followers_count)

    # שליפת כולם
    users = service.get_all_users()
    print("👥 כל היוזרים:", [usr.username for usr in users])

    # # מחיקה
    # deleted = service.delete_user("12345")
    # print("🗑️ נמחק:", deleted.user_id if deleted else "לא נמצא")
