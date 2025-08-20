from sqlalchemy import Column, String, Integer, TIMESTAMP, Enum, event
from sqlalchemy.orm import Session
import enum
from datetime import datetime, timedelta, date

from careDataBase.session import Base, engine


class TwitterTokenTypeEnum(enum.Enum):
    APP = "app"
    USER = "user"


class TwitterTokenStatusEnum(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    NOT_DOWNLOADED = "not_downloaded"


class Token(Base):
    __tablename__ = "tokens"

    token_name = Column(String, primary_key=True)
    token_type = Column(Enum(TwitterTokenTypeEnum, name="twitter_token_type"), nullable=False)
    token_status = Column(Enum(TwitterTokenStatusEnum, name="twitter_token_status"), nullable=False, server_default="ACTIVE")
    notes = Column(String, nullable=True)
    monthly_read_used = Column(Integer, nullable=False, default=0)
    monthly_reset_at = Column(TIMESTAMP, nullable=True)

    def reset_if_needed(self):
        now = datetime.utcnow()
        if self.monthly_reset_at and now >= self.monthly_reset_at:
            today = date.today()
            self.monthly_read_used = 0
            day_in_month = today.day
            self.monthly_reset_at = self.next_month(day_in_month)
            self.updated_at = now
            if self.token_status == TwitterTokenStatusEnum.NOT_DOWNLOADED:
                self.token_status = TwitterTokenStatusEnum.ACTIVE
            return True  # נעשה reset
        return False
    
    def next_month(day: int):
        today = date.today()
        if today.day < day:
            return date(today.year, today.month, day)
        else:
            if today.month == 12:  # סוף שנה
                return date(today.year + 1, 1, day)
            else:
                return date(today.year, today.month + 1, day)
        
    def chck_if_active(self):
        if self.token_status == TwitterTokenStatusEnum.ACTIVE and self.monthly_read_used > self.monthly_read_limit:
            self.token_status = TwitterTokenStatusEnum.NOT_DOWNLOADED
            return False
        return True


# 🟢 event: נטען אובייקט → נבדוק reset
@event.listens_for(Token, "load")
def auto_reset_on_load(target: Token, context):
    if target.reset_if_needed():
        session = context.session
        if session:
            session.add(target)  # מסמן אותו כ-dirty → ישמר אוטומטית


# 🟢 event: refresh (session.refresh או lazy load)
@event.listens_for(Token, "refresh")
def auto_reset_on_refresh(target: Token, context, attrs):
    if target.reset_if_needed():
        session = context.session
        if session:
            session.add(target)


# 🟢 event: אחרי flush – אם נעשו שינויים, נשמור אוטומטית
@event.listens_for(Session, "after_flush")
def auto_commit_after_flush(session, flush_context):
    if session.dirty:  # אם יש שינויים
        session.commit()


@event.listens_for(Token, "load")
def auto_check_on_load(token, context):
    # מריץ את הבדיקה
    changed = token.chck_if_active()
    if changed is False:  # אם הסטטוס השתנה
        session = context.session
        if session is not None:
            session.add(token)   # מסמן שהטוקן השתנה
            session.commit()     # שומר מיידית ב־DB