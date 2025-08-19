from careDataBase.session import Base, engine
from careDataBase.models.tokens import Token
from careDataBase.models.users import User
from careDataBase.models.user_state import UserState
from careDataBase.models.tokens_endpoints_rl import TokensEndpointRL
from careDataBase.models.twitts import Tweet
from careDataBase.models.api_calls import ApiCall
from sqlalchemy import create_engine

__all__ = [
    "Base",
    "Token",
    "User",
    "UserState",
    "TokensEndpointRL",
    "Tweet",
    "ApiCall",
]

# יצירת הטבלאות 
if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables are ready")