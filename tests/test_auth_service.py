"""
Tests pour AuthService - digicheese-api
Tests d'authentification et JWT
"""

import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.auth_service import AuthService
from src.models.user import User, UserCreate
from src.schemas.auth import LoginRequest


def test_register_user_success():
    """Test enregistrement d'un nouvel utilisateur"""
    mock_session = Mock(spec=Session)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'), \
         patch('src.services.auth_service.get_password_hash', return_value="hashed_password"):
        
        service = AuthService(mock_session)
        result = service.register_user(user_data)
        
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.hashed_password == "hashed_password"


def test_login_success():
    """Test connexion avec identifiants valides"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    login_data = LoginRequest(username="testuser", password="password123")
    
    with patch.object(mock_session, 'exec', return_value=[mock_user]), \
         patch('src.services.auth_service.verify_password', return_value=True), \
         patch('src.services.auth_service.create_access_token', return_value="jwt_token"):
        
        service = AuthService(mock_session)
        result = service.login(login_data)
        
        assert result.access_token == "jwt_token"
        assert result.token_type == "bearer"


def test_login_invalid_password():
    """Test connexion avec mot de passe invalide"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    login_data = LoginRequest(username="testuser", password="wrongpassword")
    
    with patch.object(mock_session, 'exec', return_value=[mock_user]), \
         patch('src.services.auth_service.verify_password', return_value=False):
        
        service = AuthService(mock_session)
        
        with pytest.raises(Exception):  # Should raise InvalidCredentialsException
            service.login(login_data)


def test_login_user_not_found():
    """Test connexion avec utilisateur inexistant"""
    mock_session = Mock(spec=Session)
    login_data = LoginRequest(username="nonexistent", password="password123")
    
    with patch.object(mock_session, 'exec', return_value=[]):
        service = AuthService(mock_session)
        
        with pytest.raises(Exception):  # Should raise InvalidCredentialsException
            service.login(login_data)


def test_get_current_user_success():
    """Test récupération de l'utilisateur courant"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'get', return_value=mock_user):
        service = AuthService(mock_session)
        result = service.get_current_user(1)
        
        assert result.id == 1
        assert result.username == "testuser"


def test_refresh_token_success():
    """Test rafraîchissement du token JWT"""
    mock_session = Mock(spec=Session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    with patch.object(mock_session, 'get', return_value=mock_user), \
         patch('src.services.auth_service.create_access_token', return_value="new_jwt_token"):
        
        service = AuthService(mock_session)
        result = service.refresh_token(1)
        
        assert result.access_token == "new_jwt_token"
        assert result.token_type == "bearer"
