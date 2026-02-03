"""
Tests pour ConditionnementItemService - digicheese-api
Tests de gestion des conditionnements d'items
"""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.conditionnement_service import ConditionnementItemService
from src.models.conditionnement import ConditionnementItem, ConditionnementCreate, ConditionnementUpdate


def test_create_conditionnement_success():
    """Test création d'un conditionnement avec succès"""
    mock_session = Mock(spec=Session)
    conditionnement_data = ConditionnementCreate(
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = ConditionnementItemService(mock_session)
        result = service.create_conditionnement(conditionnement_data)
        
        assert result.item_id == 1
        assert result.type_conditionnement == "boite"
        assert result.quantite_par_conditionnement == 12
        assert result.prix_conditionnement == 15.99


def test_get_conditionnement_by_id_success():
    """Test récupération d'un conditionnement par ID"""
    mock_session = Mock(spec=Session)
    mock_conditionnement = ConditionnementItem(
        id=1,
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    
    with patch.object(mock_session, 'get', return_value=mock_conditionnement):
        service = ConditionnementItemService(mock_session)
        result = service.get_conditionnement_by_id(1)
        
        assert result.id == 1
        assert result.item_id == 1
        assert result.type_conditionnement == "boite"


def test_get_conditionnements_by_item():
    """Test récupération des conditionnements d'un item"""
    mock_session = Mock(spec=Session)
    mock_conditionnements = [
        ConditionnementItem(id=1, item_id=1, type_conditionnement="boite", quantite_par_conditionnement=12, prix_conditionnement=15.99),
        ConditionnementItem(id=2, item_id=1, type_conditionnement="carton", quantite_par_conditionnement=120, prix_conditionnement=150.99)
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_conditionnements):
        service = ConditionnementItemService(mock_session)
        result = service.get_conditionnements_by_item(1)
        
        assert len(result) == 2
        assert result[0].item_id == 1
        assert result[1].item_id == 1


def test_update_conditionnement_success():
    """Test mise à jour d'un conditionnement"""
    mock_session = Mock(spec=Session)
    mock_conditionnement = ConditionnementItem(
        id=1,
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    update_data = ConditionnementUpdate(
        quantite_par_conditionnement=15,
        prix_conditionnement=18.99
    )
    
    with patch.object(mock_session, 'get', return_value=mock_conditionnement), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = ConditionnementItemService(mock_session)
        result = service.update_conditionnement(1, update_data)
        
        assert result.quantite_par_conditionnement == 15
        assert result.prix_conditionnement == 18.99


def test_delete_conditionnement_success():
    """Test suppression d'un conditionnement"""
    mock_session = Mock(spec=Session)
    mock_conditionnement = ConditionnementItem(
        id=1,
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    
    with patch.object(mock_session, 'get', return_value=mock_conditionnement), \
         patch.object(mock_session, 'delete'), \
         patch.object(mock_session, 'commit'):
        
        service = ConditionnementItemService(mock_session)
        result = service.delete_conditionnement(1)
        
        assert result is True


def test_get_all_conditionnements():
    """Test récupération de tous les conditionnements"""
    mock_session = Mock(spec=Session)
    mock_conditionnements = [
        ConditionnementItem(id=1, item_id=1, type_conditionnement="boite", quantite_par_conditionnement=12, prix_conditionnement=15.99),
        ConditionnementItem(id=2, item_id=2, type_conditionnement="sachet", quantite_par_conditionnement=5, prix_conditionnement=8.99),
        ConditionnementItem(id=3, item_id=3, type_conditionnement="carton", quantite_par_conditionnement=50, prix_conditionnement=75.99)
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_conditionnements):
        service = ConditionnementItemService(mock_session)
        result = service.get_all_conditionnements()
        
        assert len(result) == 3
        assert result[0].type_conditionnement == "boite"
        assert result[1].type_conditionnement == "sachet"
        assert result[2].type_conditionnement == "carton"


def test_calculate_prix_unitaire():
    """Test calcul du prix unitaire d'un conditionnement"""
    mock_session = Mock(spec=Session)
    mock_conditionnement = ConditionnementItem(
        id=1,
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    
    service = ConditionnementItemService(mock_session)
    prix_unitaire = service.calculate_prix_unitaire(mock_conditionnement)
    
    assert prix_unitaire == 1.3325  # 15.99 / 12


def test_conditionnement_exists():
    """Test vérification si un conditionnement existe"""
    mock_session = Mock(spec=Session)
    mock_conditionnement = ConditionnementItem(
        id=1,
        item_id=1,
        type_conditionnement="boite",
        quantite_par_conditionnement=12,
        prix_conditionnement=15.99
    )
    
    with patch.object(mock_session, 'exec', return_value=[mock_conditionnement]):
        service = ConditionnementItemService(mock_session)
        result = service.conditionnement_exists(1, "boite")
        
        assert result is True
