from sqlalchemy.orm import Session
from app.domain.models import User
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
def get_by_email(self, email: str) -> Optional[User]:
    return self.db.query(User).filter(User.email == email).first()

def create(self, email: str, password_hash: str) -> User:
    user = User(email=email, password_hash=password_hash)
    self.db.add(user)
    self.db.flush() 
    return user

def increment_failed(self, user: User):
    user.failed_attempts += 1
    self.db.add(user)

    def reset_failed(self, user: User):
        user.failed_attempts = 0
        user.locked_until = None
        self.db.add(user)