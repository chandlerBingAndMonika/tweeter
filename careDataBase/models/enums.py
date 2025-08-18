import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'http_method') THEN
        CREATE TYPE http_method AS ENUM ('GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'twitter_token_type') THEN
        CREATE TYPE twitter_token_type AS ENUM ('free','basic','pro','enterprise','essential','elevated','academic');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'twitter_token_status') THEN
        CREATE TYPE twitter_token_status AS ENUM ('active','invalid','revoked','rate_limited','unknown');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tweet_type_enum') THEN
        CREATE TYPE tweet_type_enum AS ENUM ('original','reply','retweet','quote');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status_enum') THEN
        CREATE TYPE task_status_enum AS ENUM ('pending','running','done','failed','partial');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_item_status_enum') THEN
        CREATE TYPE task_item_status_enum AS ENUM ('pending','running','done','failed','retry');
    END IF;
END$$;
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ enums ready")
