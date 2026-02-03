"""
Tests pour UserService - digicheese-api
Tests de gestion des utilisateurs
"""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.user_service import UserService
from src.models.user import User, UserCreate, UserUpdate


def test_create_user_success():
    """Test création d'un utilisateur avec succès"""
    mock_session = Mock(spec=Session)
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="password123"
    )
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'), \
         patch('src.services.user_service.get_password_hash', return_value="hashed_password"):
        
        service = UserService(mock_session)
        result = service.create_user(user_data)
        
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        assert result.hashed_password == "hashed_password"


def test_get_user_by_id_success():
    """Test récupération d'un utilisateur par ID"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'get', return_value=mock_user):
        service = UserService(mock_session)
        result = service.get_user_by_id(1)
        
        assert result.id == 1
        assert result.username == "testuser"


def test_get_user_by_username_success():
    """Test récupération d'un utilisateur par username"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'exec', return_value=[mock_user]):
        service = UserService(mock_session)
        result = service.get_user_by_username("testuser")
        
        assert result.username == "testuser"
        assert result.email == "test@example.com"


def test_get_users_list():
    """Test récupération de la liste des utilisateurs"""
    mock_session = Mock(spec=Session)
    mock_users = [
        User(id=1, username="user1", email="user1@example.com", hashed_password="hash1"),
        User(id=2, username="user2", email="user2@example.com", hashed_password="hash2")
    ]
    
    with patch.object(mock_session, 'exec', return_value=mock_users):
        service = UserService(mock_session)
        result = service.get_users()
        
        assert len(result) == 2
        assert result[0].username == "user1"
        assert result[1].username == "user2"


def test_update_user_success():
    """Test mise à jour d'un utilisateur"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="olduser",
        email="old@example.com",
        hashed_password="hashed_password"
    )
    update_data = UserUpdate(username="newuser", email="new@example.com")
    
    with patch.object(mock_session, 'get', return_value=mock_user), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        
        service = UserService(mock_session)
        result = service.update_user(1, update_data)
        
        assert result.username == "newuser"
        assert result.email == "new@example.com"


def test_delete_user_success():
    """Test suppression d'un utilisateur"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'get', return_value=mock_user), \
         patch.object(mock_session, 'delete'), \
         patch.object(mock_session, 'commit'):
        
        service = UserService(mock_session)
        result = service.delete_user(1)
        
        assert result is True


def test_user_exists_true():
    """Test vérification si utilisateur existe (vrai)"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'exec', return_value=[mock_user]):
        service = UserService(mock_session)
        result = service.user_exists("testuser")
        
        assert result is True


def test_user_exists_false():
    """Test vérification si utilisateur existe (faux)"""
    mock_session = Mock(spec=Session)
    
    with patch.object(mock_session, 'exec', return_value=[]):
        service = UserService(mock_session)
        result = service.user_exists("nonexistent")
        
        assert result is False
