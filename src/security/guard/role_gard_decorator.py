from functools import wraps
from typing import Callable, Any, Dict
from fastapi import Depends, HTTPException, status, Request

from src.enum.role_enum import RoleEnum
import inspect
from src.security.auth import get_current_user


def is_granted(*allowed_roles: RoleEnum) -> Callable:
    allowed_set = {role.name.upper() for role in allowed_roles}

    def decorator(endpoint: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(endpoint)
        async def wrapper(*args: Any, current_user: Dict = Depends(get_current_user), **kwargs: Any):

            user_roles = {r.name for r in current_user.get("roles", [])}

            if user_roles.isdisjoint(allowed_set):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accès refusé",
                )

            result = endpoint(*args, **kwargs)
            if inspect.isawaitable(result):
                return await result
            return result

        return wrapper

    return decorator