from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from careDataBase.session import Base, engine


class TokensEndpointRL(Base):
    __tablename__ = "tokens_endpoint_rl"

    token_name = Column(String, ForeignKey("tokens.token_name", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    endpoint_bucket = Column(String, primary_key=True)
    rl_reset_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=False, server_default="now()")
    remaining_requests = Column(Integer, nullable=False, default=0)