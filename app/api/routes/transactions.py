from fastapi import APIRouter, Depends
from app.services.transaction_service import TransactionService
from app.domain.schemas import WithdrawRequest

router = APIRouter()

@router.post("/withdraw")
def withdraw(
    data: WithdrawRequest,
    service: TransactionService = Depends()
):
    return service.withdraw(
        account_id=data.account_id,
        amount=data.amount
    )