from sqlalchemy import create_engine, text

from config import settings


engine = create_engine(url=settings.database_url_psycopg)


def get_db_version() -> str:
    with engine.connect() as conn:
        res = conn.execute(text('SELECT VERSION()'))
        return f'{res.first()[0]=}'
