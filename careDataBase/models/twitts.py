import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
CREATE TABLE IF NOT EXISTS tweets (
  tweet_id              TEXT PRIMARY KEY,
  user_id               TEXT NOT NULL REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  created_at            TIMESTAMPTZ NOT NULL,
  text                  TEXT,
  like_count            INTEGER,
  retweet_count         INTEGER,
  reply_count           INTEGER,
  quote_count           INTEGER,
  tweet_type            tweet_type_enum NOT NULL,
  in_reply_to_user_id   TEXT,
  referenced_retweet_id TEXT,
  referenced_reply_id   TEXT,
  api_call_id           BIGINT REFERENCES api_calls(id) ON UPDATE CASCADE ON DELETE SET NULL,
  raw_json              JSONB NOT NULL,
  ingested_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tweets_user_time ON tweets (user_id, created_at DESC);
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ tweets table ready")
