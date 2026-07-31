from typing import List, Optional

from .models import Expense


expenses: List[Expense] = []


def get_all_expenses() -> List[Expense]:
    return expenses


def add_expense(expense: Expense) -> Expense:
    expenses.append(expense)
    return expense


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    for expense in expenses:
        if expense.id == expense_id:
            return expense

    return None


def delete_expense(expense_id: int) -> bool:
    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            expenses.pop(index)
            return True

    return False