from fastapi import APIRouter, HTTPException, status
from typing import Optional
from . import storage
from .models import Expense, ExpenseCreate


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post(
    "",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(expense_data: ExpenseCreate):
    return storage.add_expense(expense_data)

@router.get("", response_model=list[Expense])
def get_expenses(category: Optional[str] = None):
    if category:
        return storage.get_expenses_by_category(category)

    return storage.get_all_expenses()

@router.get("/summary")
def get_summary():
    return storage.get_expense_summary()

@router.get("/summary/monthly")
def get_monthly_summary(year: int, month: int):
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12",
        )
    return storage.get_monthly_summary(year, month)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    deleted = storage.delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )