from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url_psycopg)

session_maker = sessionmaker(engine)


def get_db() -> Iterator[Session]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
