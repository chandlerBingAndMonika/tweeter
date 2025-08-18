import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
CREATE TABLE IF NOT EXISTS tokens (
  token_name              TEXT PRIMARY KEY,
  token_type              twitter_token_type NOT NULL,
  token_status            twitter_token_status NOT NULL DEFAULT 'active',
  is_active               BOOLEAN NOT NULL DEFAULT TRUE,
  owner_label             TEXT,
  notes                   TEXT,
  monthly_read_limit      INTEGER,
  monthly_read_used       INTEGER NOT NULL DEFAULT 0,
  monthly_reset_at        TIMESTAMPTZ,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ tokens table ready")
