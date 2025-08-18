import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
CREATE TABLE IF NOT EXISTS user_state (
  user_id                        TEXT PRIMARY KEY REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  last_seen_id                   TEXT,
  oldest_downloaded_tweet_id     TEXT,
  downloaded_tweets_count        INTEGER NOT NULL DEFAULT 0,
  total_tweets_count             INTEGER NOT NULL DEFAULT 0,
  is_limited_access              BOOLEAN NOT NULL DEFAULT FALSE,
  is_tracked                     BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at                     TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ user_state table ready")
