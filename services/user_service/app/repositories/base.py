# pylint: disable=E0211:no-method-argument

from abc import ABC, abstractmethod

from sqlalchemy import insert

from app.db.db import session_maker


class AbstractRepository(ABC):
    @abstractmethod
    def add_one():
        raise NotImplementedError

    @abstractmethod
    def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def add_one(self, data: dict) -> int:
        with session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = session.execute(stmt)
            session.commit()
            return res.scalar_one()

    def get_all(self):
        pass
