from sqlalchemy import create_engine
from base import Base

# לייבא את המודלים כדי שיירשמו ל-Base.metadata:
import callTwitterModel, tokenModel, twittModel, userTwiterModel

engine = create_engine("postgresql+psycopg2://user:pass@host:5432/dbname", echo=True)
Base.metadata.create_all(engine)
print("OK – tables created or already exist.")
