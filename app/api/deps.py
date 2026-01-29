# app/api/deps.py (trecho)
from fastapi import Request, HTTPException, Depends
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Sem sessão")
    return token

def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_session_token_from_cookie)):
    session_repo = SessionRepository(db)
    session = session_repo.get(token)
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Sessão inválida")
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(session.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuário inválido")
    return user
