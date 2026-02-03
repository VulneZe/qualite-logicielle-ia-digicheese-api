import time
from datetime import datetime, timezone, timedelta
from typing import Any, List, Dict

from fastapi import HTTPException, status, Request, Response, Depends
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src import User, RoleEnum
from src.config.jwt_config import PUBLIC_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, PRIVATE_KEY, REFRESH_TOKEN_EXPIRE_DAYS
import jwt
from src.security.middleware import blacklist_jti
from uuid import uuid4

hasher = PasswordHasher()


def get_current_user(request: Request) -> Dict:
    user_payload = getattr(request.state, "user", None)
    refresh_token = request.cookies.get("refresh_token")

    if not user_payload or not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Non authentifié",
        )

    refresh_decoded = Auth.jwt_decode(refresh_token)
    sub = user_payload["id"]
    sub_refresh = refresh_decoded.get("sub")

    if sub != sub_refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
        )

    if user_payload['roles'] != refresh_decoded.get('roles'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
        )

    user_roles = set()
    for role in refresh_decoded.get("roles", []):

        if isinstance(role, RoleEnum):
            user_roles.add(role.name.upper())
        elif isinstance(role, str):
            user_roles.add(role.upper())
        else:
            # fallback
            user_roles.add(str(role).upper())

    current_user = dict(id=sub_refresh, roles=[RoleEnum[role] for role in user_roles])

    return current_user


class Auth:

    @staticmethod
    def password_hash(password: str) -> str:
        return hasher.hash(password)

    @staticmethod
    def verify_password(plain_password: str, password_hash: str) -> bool:
        try:
            return hasher.verify(password_hash, plain_password)
        except VerifyMismatchError:
            return False

    def refresh_token(self, refresh_token: str, response: Response) -> str:
        try:
            payload = jwt.decode(
                refresh_token,
                PUBLIC_KEY,
                algorithms=[ALGORITHM],
                options={"verify_aud": False}
            )
            # Vérifications critiques
            if payload.get("type") != "refresh_token":
                raise HTTPException(status_code=401, detail="Invalid credentials")
            if payload.get("jti") in blacklist_jti:
                raise HTTPException(status_code=401, detail="No Token found. Token must be revoked")
            if payload.get("exp") < time.time():
                raise HTTPException(status_code=401, detail="No Token found. Token must be expired")
            # Rotation
            blacklist_jti.add(payload["jti"])
            user_id = payload["sub"]
            roles = payload["roles"]
            access_token = self.create_access_token(user_id, roles)
            new_refresh_token = self.create_refresh_token(user_id, roles)
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=7 * 24 * 3600,
                path="/"
            )
            return access_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def erase_credentials(request: Request, response: Response) -> None:
        user_payload = getattr(request.state, "user", None) or None
        token = request.cookies.get("refresh_token")

        refresh_token = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )

        jti = user_payload.get("jti") if user_payload is not None else None
        jti_refresh = refresh_token.get("jti")

        if jti or jti_refresh:
            blacklist_jti.add(jti)
            blacklist_jti.add(jti_refresh)

        response.delete_cookie("refresh_token")
        request.state.user = None

    # 🔽 helpers privés
    @staticmethod
    def create_access_token(user_id: int, roles: list[str]) -> str:
        payload = {
            "sub": str(user_id),
            "roles": roles,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "jti": str(uuid4()),
            "type": "access_token",
        }
        return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: int, roles: list[str]) -> str:
        payload = {
            "sub": str(user_id),
            "roles": roles,
            "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "jti": str(uuid4()),
            "type": "refresh_token",
        }
        return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

    @staticmethod
    def jwt_decode(token: str) -> Dict[str, Any]:
        return jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )

    @staticmethod
    def jwt_encode(user_id: int, roles: List[str]) -> List:
        payload = {
            "sub": str(user_id),
            "roles": roles,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "jti": str(uuid4()),
            "type": "access_token",
        }

        return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
