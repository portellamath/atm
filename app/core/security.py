from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BCRYPT_ROUNDS = 12

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_session_token() -> str:
    return str(uuid.uuid4())

def now_plus_minutes(minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)