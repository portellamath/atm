from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_session_token_from_cookie
from app.services.auth_service import AuthService
from pydantic import BaseModel, EmailStr
from datetime import datetime

router = APIRouter()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        with db.begin():
            user = service.register(data.email, data.password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginIn, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        with db.begin():
            res = service.login(data.email, data.password)
            response.set_cookie(
                key="session_token",
                value=res["token"],
                httponly=True,
                secure=True,
                samesite="lax",
                expires=int((res["expires_at"] - datetime.utcnow()).total_seconds())
            )
        return {"user_id": res["user_id"]}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db), session_token: str = Depends(get_session_token_from_cookie)):
    service = AuthService(db)
    with db.begin():
        service.logout(session_token)
        response.delete_cookie("session_token")
    return {"ok": True} 