from typing import Any, List
from urllib import response
from urllib.request import Request

from .. import User, Auth, Role
from fastapi import HTTPException, status, Response, Depends
from ..repositories.user_repository import UserRepository
from sqlmodel import Session
from argon2 import PasswordHasher

from ..security.auth import get_current_user


class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)
        self.auth = Auth()

    def authenticate(self, username: str, password: str, response: Response) -> str:
        user: User | None = self.user_repo.get_user_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not self.auth.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        roles: list[str] = [role.name.value for role in user.roles]

        token = self.auth.create_access_token(user.id, roles)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        self.create_session( user, roles, self.auth, response)

        return token

    def refresh(self, refresh_token: str, response: Response) -> str:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        return self.auth.refresh_token(refresh_token, response)

    def logout(self, request: Request, response: Response) -> None:

        if not request.cookies.get("refresh_token"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        self.auth.erase_credentials(request, response)

    @staticmethod
    def create_session(user: User, roles: List, auth: Auth, response: Response) -> Response:
        token = auth.create_refresh_token(user.id, roles)

        return response.set_cookie(
            key="refresh_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7 * 24 * 3600,
            path="/"
        )
