from abc import ABC, abstractmethod
from sqlalchemy.exc import NoResultFound


class AbstractRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, item_id):
        raise NotImplementedError

    @abstractmethod
    def add(self, item):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, item_id, data: dict):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, item_id):
        raise NotImplementedError
    

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_all(self):
        return self.session.query(self.model).all()
    
    def get_by_id(self, item_id):
        return self.session.query(self.model).get(item_id)
    
    def add(self, item):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, item_id, data: dict):
        item = self.get_by_id(item_id)
        if not item:
            raise NoResultFound(f"{self.model.__name__} not found")
        
        for key, value in data.items():
            setattr(item, key, value)

        self.session.add(item)
        self.session.commit()
        return item

    def delete(self, item_id):
        item = self.get_by_id(item_id)
        if not item:
            raise NoResultFound(f"{self.model.__name__} not found")
        
        self.session.delete(item)
        self.session.commit()