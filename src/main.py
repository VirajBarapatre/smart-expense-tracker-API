from typing import List, Optional
from uuid import UUID
from fastapi import FastAPI, HTTPException, Query, status
from src.models import Expense, ExpenseCreate, ExpenseSummary
from src.storage import ExpenseStorage
from fastapi.responses import RedirectResponse



app = FastAPI(
    title="Smart Expense Tracker API",
    description="API for tracking personal expenses, calculating totals, and filtering categories.",
    version="1.0.0",
)

storage = ExpenseStorage(filepath="expenses.json")


@app.post(
    "/expenses",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new expense",
)
def create_expense(expense: ExpenseCreate):
    return storage.add_expense(expense)


@app.get(
    "/expenses",
    response_model=List[Expense],
    summary="View all expenses (optional category filter)",
)
def list_expenses(category: Optional[str] = Query(None, description="Filter expenses by category")):
    return storage.get_all(category=category)


@app.get(
    "/expenses/summary",
    response_model=ExpenseSummary,
    summary="Calculate total expenses overall, by category, and monthly",
)
def get_expense_summary():
    return storage.get_summary()


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense by ID",
)
def delete_expense(expense_id: UUID):
    success = storage.delete_expense(expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )
    return None

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")