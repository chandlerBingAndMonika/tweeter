from sqlalchemy.orm import Session
from careDataBase.session import SessionLocal
from careDataBase.models.tokens import Token, TwitterTokenTypeEnum, TwitterTokenStatusEnum

class TokenService:
    def __init__(self):
        self.db: Session = SessionLocal()

    # 🟢 Create
    def create_token(
        self,
        token_name: str,
        token_type: TwitterTokenTypeEnum,
        token_status: TwitterTokenStatusEnum = TwitterTokenStatusEnum.ACTIVE,
        notes: str = None,
        monthly_read_limit: int = None,
        monthly_read_used: int = 0,
        monthly_reset_at=None
    ):
        token = Token(
            token_name=token_name,
            token_type=token_type,
            token_status=token_status,
            notes=notes,
            monthly_read_limit=monthly_read_limit,
            monthly_read_used=monthly_read_used,
            monthly_reset_at=monthly_reset_at
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    # 🔵 Read - get one
    def get_token(self, token_name: str):
        return self.db.query(Token).filter(Token.token_name == token_name).first()

    # 🔵 Read - get all
    def get_all_tokens(self):
        return self.db.query(Token).all()

    # 🟠 Update
    def update_token(self, token_name: str, **kwargs):
        token = self.get_token(token_name)
        if not token:
            return None
        for key, value in kwargs.items():
            if hasattr(token, key):
                setattr(token, key, value)
        self.db.commit()
        self.db.refresh(token)
        return token

    # 🔴 Delete
    def delete_token(self, token_name: str):
        token = self.get_token(token_name)
        if not token:
            return None
        self.db.delete(token)
        self.db.commit()
        return token

