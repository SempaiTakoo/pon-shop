from app.repository.base import SqlAlchemyRepository
from app.db.models import Order


class OrderRepository(SqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, Order)