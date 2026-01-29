from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.core.security import hash_password, verify_password, create_session_token, now_plus_minutes

MAX_FAILED = 5
LOCKOUT_MINUTES = 15
SESSION_TTL_MINUTES = 60 * 8

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.session_repo = SessionRepository(db)

    def register(self, email: str, password: str):
        if self.user_repo.get_by_email(email):
            raise ValueError("Email já está cadastrado")
        pw_hash = hash_password(password)
        user = self.user_repo.create(email=email, password_hash=pw_hash)
        return user

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active:
            raise ValueError("Credenciais inválidas")

        if user.locked_until and user.locked_until > datetime.utcnow():
            raise ValueError("Conta temporariamente bloqueada")

        if not verify_password(password, user.password_hash):
            self.user_repo.increment_failed(user)
            if (user.failed_attempts or 0) + 1 >= MAX_FAILED:
                user.locked_until = now_plus_minutes(LOCKOUT_MINUTES)
            raise ValueError("Credenciais inválidas")

        self.user_repo.reset_failed(user)
        token = create_session_token()
        expires = now_plus_minutes(SESSION_TTL_MINUTES)
        session = self.session_repo.create(token, user.id, expires)
        return {"token": token, "expires_at": expires, "user_id": user.id}

    def logout(self, token: str):
        self.session_repo.delete(token)