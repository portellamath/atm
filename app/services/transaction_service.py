from decimal import Decimal
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(
        self,
        account_repo: AccountRepository,
        transaction_repo: TransactionRepository
    ):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def withdraw(self, account_id: int, amount: Decimal):
        account = self.account_repo.get_by_id(account_id)

        if account.balance < amount:
            raise ValueError("Saldo insuficiente")

        account.balance -= amount
        self.transaction_repo.create_withdraw(account_id, amount)