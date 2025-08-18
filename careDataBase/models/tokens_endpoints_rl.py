import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=True)

SQL = """
CREATE TABLE IF NOT EXISTS tokens_endpoint_rl (
  token_name      TEXT NOT NULL REFERENCES tokens(token_name) ON UPDATE CASCADE ON DELETE CASCADE,
  endpoint_bucket TEXT NOT NULL,
  rl_limit        INTEGER,
  rl_remaining    INTEGER,
  rl_reset_at     TIMESTAMPTZ,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (token_name, endpoint_bucket)
);
"""

with engine.begin() as conn:
    conn.exec_driver_sql(SQL)
print("✅ tokens_endpoint_rl table ready")
