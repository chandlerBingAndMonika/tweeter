from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from careDataBase.session import Base, engine

class TokensEndpointRL(Base):
    __tablename__ = "tokens_endpoint_rl"

    token_name = Column(String, ForeignKey("tokens.token_name", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    endpoint_bucket = Column(String, primary_key=True)
    rl_limit = Column(Integer, nullable=True)
    rl_remaining = Column(Integer, nullable=True)
    rl_reset_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=False, server_default="now()")

# יצירת הטבלה
if __name__ == "__main__":
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    print("✅ tokens_endpoint_rl table ready")
