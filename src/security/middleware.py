from typing import List, Callable, Awaitable

from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse
import jwt
import src.config.jwt_config as jwt_config

blacklist_jti = set()

async def jwt_validation_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    auth = request.headers.get("Authorization")
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return await call_next(request)

    if not auth or not auth.startswith("Bearer "):
        return await call_next(request)

    token = auth.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, jwt_config.PUBLIC_KEY, algorithms=[jwt_config.ALGORITHM], options={"verify_aud": False})
        refresh_payload = jwt.decode(refresh_token, jwt_config.PUBLIC_KEY, algorithms=[jwt_config.ALGORITHM], options={"verify_aud": False})

        if payload.get("jti") and refresh_payload.get("jti") in blacklist_jti:
            return JSONResponse({"detail": "Invalid credentials"}, status_code=401)

        roles = payload.get("roles", [])

        if roles != refresh_payload.get("roles", []) and payload.get("sud") != refresh_payload.get("sub"):
            return JSONResponse({"detail": "Invalid credentials"}, status_code=401)

        # Normalisation : si c'est une string
        if isinstance(roles, str):
            roles = [roles]

        request.state.user = {
            "id": payload.get("sub"),
            "roles": roles,
            "jti": payload.get("jti"),
        }

    except jwt.ExpiredSignatureError:
        return JSONResponse({"detail": "No token found. Token must be expired"}, status_code=401)
    except jwt.InvalidTokenError:
        return JSONResponse({"detail": "Invalid crédentials"}, status_code=401)

    return await call_next(request)
