from fastapi import APIRouter, HTTPException, status

from . import storage
from .models import Expense, ExpenseCreate


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post(
    "",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(expense_data: ExpenseCreate):
    expense_id = len(storage.get_all_expenses()) + 1

    expense = Expense(
        id=expense_id,
        **expense_data.model_dump(),
    )

    return storage.add_expense(expense)


@router.get("", response_model=list[Expense])
def get_expenses():
    return storage.get_all_expenses()


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    deleted = storage.delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )