"""
Tests pour OrderService - digicheese-api
Tests de gestion des commandes
"""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.order_service import OrderService
from src.models.order import Order, OrderCreate, OrderUpdate
from src.models.order_item import OrderItem
from datetime import datetime


def test_create_order_success():
    """Test création d'une commande avec succès"""
    mock_session = Mock(spec=Session)
    order_data = OrderCreate(
        user_id=1,
        items=[
            {"item_id": 1, "quantity": 2, "price": 10.99},
            {"item_id": 2, "quantity": 1, "price": 20.99}
        ]
    )
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = OrderService(mock_session)
        result = service.create_order(order_data)
        
        assert result.user_id == 1
        assert len(result.items) == 2


def test_get_order_by_id_success():
    """Test récupération d'une commande par ID"""
    mock_session = Mock(spec=Session)
    mock_order = Order(
        id=1,
        user_id=1,
        status="pending",
        total_amount=42.97,
        created_at=datetime.now()
    )
    
    with patch.object(mock_session, 'get', return_value=mock_order):
        service = OrderService(mock_session)
        result = service.get_order_by_id(1)
        
        assert result.id == 1
        assert result.user_id == 1
        assert result.status == "pending"


def test_get_orders_by_user():
    """Test récupération des commandes d'un utilisateur"""
    mock_session = Mock(spec=Session)
    mock_orders = [
        Order(id=1, user_id=1, status="pending", total_amount=42.97),
        Order(id=2, user_id=1, status="completed", total_amount=15.99)
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_orders):
        service = OrderService(mock_session)
        result = service.get_orders_by_user(1)
        
        assert len(result) == 2
        assert result[0].user_id == 1
        assert result[1].user_id == 1


def test_update_order_status():
    """Test mise à jour du statut d'une commande"""
    mock_session = Mock(spec=Session)
    mock_order = Order(
        id=1,
        user_id=1,
        status="pending",
        total_amount=42.97
    )
    update_data = OrderUpdate(status="completed")
    
    with patch.object(mock_session, 'get', return_value=mock_order), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = OrderService(mock_session)
        result = service.update_order(1, update_data)
        
        assert result.status == "completed"


def test_cancel_order_success():
    """Test annulation d'une commande"""
    mock_session = Mock(spec=Session)
    mock_order = Order(
        id=1,
        user_id=1,
        status="pending",
        total_amount=42.97
    )
    
    with patch.object(mock_session, 'get', return_value=mock_order), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = OrderService(mock_session)
        result = service.cancel_order(1)
        
        assert result.status == "cancelled"


def test_calculate_order_total():
    """Test calcul du total d'une commande"""
    mock_session = Mock(spec=Session)
    order_items = [
        OrderItem(item_id=1, quantity=2, price=10.99),
        OrderItem(item_id=2, quantity=1, price=20.99)
    ]
    
    service = OrderService(mock_session)
    total = service.calculate_order_total(order_items)
    
    assert total == 42.97  # (2 * 10.99) + (1 * 20.99)


def test_get_pending_orders():
    """Test récupération des commandes en attente"""
    mock_session = Mock(spec=Session)
    mock_orders = [
        Order(id=1, user_id=1, status="pending", total_amount=42.97),
        Order(id=2, user_id=2, status="pending", total_amount=15.99)
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_orders):
        service = OrderService(mock_session)
        result = service.get_pending_orders()
        
        assert len(result) == 2
        assert all(order.status == "pending" for order in result)


def test_add_item_to_order():
    """Test ajout d'un item à une commande existante"""
    mock_session = Mock(spec=Session)
    mock_order = Order(id=1, user_id=1, status="pending", total_amount=42.97)
    
    with patch.object(mock_session, 'get', return_value=mock_order), \
         patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = OrderService(mock_session)
        result = service.add_item_to_order(1, 3, 1, 5.99)
        
        assert result is True
