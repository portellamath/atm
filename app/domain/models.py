from sqlalchemy import Column, integer, String, Boolean, DataTime
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class User(Base):
    _tablename_ = "users"

    id = Column(integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DataTime(timezone=True), server_default=func.now())

class AccountStatus(enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

class Account(Base):
    _tablename_ = "accounts"

    id = Column(integer, primary_key=True)
    user_id = Column(integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

class Transaction(Base):
    _tablename_ = "transactions"

    id = Column(integer, primary_key=True)
    account_id = Column(integer, ForeignKey("accounts.id"), nullable=False)
    related_account_id = Column(integer, ForeignKey("accounts.id"), nullable=True)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())