import pytest
from unittest.mock import MagicMock
from app.api.schemas import OrderCreate, OrderUpdate
from app.service.order_service import OrderService, to_domain
from app.db.models import Order as ORMOrder
from app.domain.models.order import Order as DomainOrder
from datetime import datetime

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return OrderService(mock_repo)

def test_add_order(service, mock_repo):
    order_data = OrderCreate(
        product_id=1,
        buyer_id=2,
        quantity=3,
        total_price=100.0,
        status="pending"
    )
    
    orm_mock = ORMOrder(
        order_id=123,
        product_id=1,
        buyer_id=2,
        quantity=3,
        total_price=100.0,
        status="pending",
        created_at=datetime.now()
    )
    
    mock_repo.add.return_value = orm_mock
    result = service.add_order(order_data)
    
    assert isinstance(result, DomainOrder)
    assert result.order_id == 123
    mock_repo.add.assert_called_once()

def test_get_order_found(service, mock_repo):
    orm_mock = ORMOrder(
        order_id=42,
        product_id=10,
        buyer_id=5,
        quantity=2,
        total_price=50.0,
        status="paid",
        created_at=datetime.now()
    )
    mock_repo.get_by_id.return_value = orm_mock
    result = service.get_order(42)
    assert isinstance(result, DomainOrder)
    assert result.order_id == 42

def test_get_order_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = service.get_order(999)
    assert result is None

def test_update_order(service, mock_repo):
    update_data = OrderUpdate(
        quantity=5,
        total_price=150.0,
        status="shipped"
    )

    orm_updated = ORMOrder(
        order_id=1,
        buyer_id=1,
        product_id=2,
        quantity=5,
        total_price=150.0,
        status="shipped",
        created_at=datetime.now()
    )

    mock_repo.update.return_value = orm_updated
    result = service.update_order(1, update_data)

    mock_repo.update.assert_called_once_with(1, update_data.model_dump())
    assert isinstance(result, DomainOrder)
    assert result.status == "shipped"

def test_delete_order(service, mock_repo):
    service.delete_order(123)
    mock_repo.delete.assert_called_once_with(123)

def test_get_all_orders(service, mock_repo):
    orm_mock_1 = ORMOrder(order_id=1, buyer_id=1, product_id=1, quantity=1, total_price=10, status="ok", created_at=datetime.now())
    orm_mock_2 = ORMOrder(order_id=2, buyer_id=2, product_id=2, quantity=2, total_price=20, status="ok", created_at=datetime.now())
    
    mock_repo.get_all.return_value = [orm_mock_1, orm_mock_2]
    
    result = service.get_all_orders()
    
    assert isinstance(result, list)
    assert all(isinstance(o, DomainOrder) for o in result)
    assert len(result) == 2
