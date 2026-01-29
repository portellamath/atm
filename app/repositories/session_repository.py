from sqlalchemy.orm import Session
from app.domain.models import Session as SessionModel
from datetime import datetime

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

def create(self, token: str, user_id: int, expires_at: datetime): 
    s = SessionModel(id=token, user_id=user_id, expires_at=expires_at)
    self.db.add(s)
    return s 

def get(self, token: str):
    return self.db.query(SessionModel).filter(SessionModel.id == token).first()

def delete(self, token: str):
    self.db.query(SessionModel).filter(SessionModel.id == token).delete()