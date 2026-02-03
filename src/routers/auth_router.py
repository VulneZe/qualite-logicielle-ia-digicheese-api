from fastapi import APIRouter, Body, status, Depends, HTTPException, Response, Request
from sqlmodel import Session

from ..config.database import get_session
from ..schemas.auth_schema.login_schema import LoginSchema
from ..services.auth_service import AuthService
from ..security.auth import get_current_user

auth = APIRouter()

@auth.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginSchema, response: Response, session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    user_token = auth_service.authenticate(user.username, user.password, response)

    return {"access_token": f"{user_token}"}

@auth.post("/logout", response_model=dict, status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response, session: Session=Depends(get_session)):
    auth_service = AuthService(session)
    auth_service.logout(request, response)

    return {"detail": "Logout successfully"}

@auth.get("/refresh")
def refresh(request: Request, response: Response, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")

    auth_service = AuthService(session)
    access_token = auth_service.refresh(refresh_token, response)

    return {"access_token": access_token}