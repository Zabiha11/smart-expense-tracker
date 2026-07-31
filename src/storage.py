from typing import List, Optional
from collections import defaultdict
from .models import Expense
from datetime import date

expenses: List[Expense] = []
_next_id = 1

def clear_expenses() -> None:
    global _next_id

    expenses.clear()
    _next_id = 1


def get_all_expenses() -> List[Expense]:
    return expenses


def add_expense(expense_data) -> Expense:
    global _next_id

    expense = Expense(
        id=_next_id,
        **expense_data.model_dump(),
    )

    expenses.append(expense)
    _next_id += 1

    return expense

def get_expenses_by_category(category: str) -> List[Expense]:
    return [
        expense
        for expense in expenses
        if expense.category.lower() == category.lower()
    ]


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    for expense in expenses:
        if expense.id == expense_id:
            return expense

    return None

def get_expense_summary() -> dict:
    total = sum(expense.amount for expense in expenses)

    by_category = defaultdict(float)

    for expense in expenses:
        by_category[expense.category] += expense.amount

    return {
        "total": total,
        "by_category": dict(by_category),
    }
    
def get_monthly_summary(year: int, month: int) -> dict:
    monthly_expenses = [
        expense
        for expense in expenses
        if expense.date.year == year
        and expense.date.month == month
    ]

    total = sum(expense.amount for expense in monthly_expenses)

    by_category = defaultdict(float)

    for expense in monthly_expenses:
        by_category[expense.category] += expense.amount

    return {
        "year": year,
        "month": month,
        "total": total,
        "transaction_count": len(monthly_expenses),
        "by_category": dict(by_category),
    }

def delete_expense(expense_id: int) -> bool:
    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            expenses.pop(index)
            return True

    return False