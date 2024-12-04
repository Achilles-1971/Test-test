from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

url_db = {"drivername": "sqlite", "database": "practice.db"}
engine = create_engine(url=URL.create(**url_db), echo=True)

session = Session(engine)
