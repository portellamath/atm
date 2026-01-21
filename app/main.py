from fastapi import FastAPI
from app.api.routes import auth, accounts, transactions

app = FastAPI(title="ATM System")

app.include_router(auth.router, prefix="/auth")
app.include_router(accounts.router, prefix="/accounts")
app.include_router(transactions.router, prefix="/transactions")