"""
Tests pour ItemService - digicheese-api
Tests CRUD pour les items
"""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.item_service import ItemService
from src.models.item import Item, ItemCreate, ItemUpdate


def test_create_item_success():
    """Test création d'un item avec succès"""
    mock_session = Mock(spec=Session)
    item_data = ItemCreate(name="Test Item", description="Test Description", price=10.99)
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = ItemService(mock_session)
        result = service.create_item(item_data)
        
        assert result.name == "Test Item"
        assert result.description == "Test Description"
        assert result.price == 10.99


def test_get_item_by_id_success():
    """Test récupération d'un item par ID"""
    mock_session = Mock(spec=Session)
    mock_item = Item(id=1, name="Test Item", description="Test", price=10.99)
    
    with patch.object(mock_session, 'get', return_value=mock_item):
        service = ItemService(mock_session)
        result = service.get_item_by_id(1)
        
        assert result.id == 1
        assert result.name == "Test Item"


def test_get_item_by_id_not_found():
    """Test récupération d'un item inexistant"""
    mock_session = Mock(spec=Session)
    
    with patch.object(mock_session, 'get', return_value=None):
        service = ItemService(mock_session)
        
        with pytest.raises(Exception):  # Should raise ItemNotFoundException
            service.get_item_by_id(999)


def test_get_items_list():
    """Test récupération de la liste des items"""
    mock_session = Mock(spec=Session)
    mock_items = [
        Item(id=1, name="Item 1", description="Desc 1", price=10.99),
        Item(id=2, name="Item 2", description="Desc 2", price=20.99)
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_items):
        service = ItemService(mock_session)
        result = service.get_items()
        
        assert len(result) == 2
        assert result[0].name == "Item 1"
        assert result[1].name == "Item 2"


def test_update_item_success():
    """Test mise à jour d'un item"""
    mock_session = Mock(spec=Session)
    mock_item = Item(id=1, name="Old Name", description="Old", price=10.99)
    update_data = ItemUpdate(name="New Name", price=15.99)
    
    with patch.object(mock_session, 'get', return_value=mock_item), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = ItemService(mock_session)
        result = service.update_item(1, update_data)
        
        assert result.name == "New Name"
        assert result.price == 15.99


def test_delete_item_success():
    """Test suppression d'un item"""
    mock_session = Mock(spec=Session)
    mock_item = Item(id=1, name="Test Item", description="Test", price=10.99)
    
    with patch.object(mock_session, 'get', return_value=mock_item), \
         patch.object(mock_session, 'delete'), \
         patch.object(mock_session, 'commit'):
        
        service = ItemService(mock_session)
        result = service.delete_item(1)
        
        assert result is True
