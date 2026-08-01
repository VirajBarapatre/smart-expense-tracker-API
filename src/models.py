from datetime import date as DateType
from typing import Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Brief description of the expense")
    amount: float = Field(..., gt=0, description="Amount spent (must be greater than 0)")
    category: str = Field(..., min_length=1, description="Category (e.g., Food, Transport)")
    date: DateType = Field(..., description="Date of the expense (YYYY-MM-DD)")


class Expense(ExpenseCreate):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the expense")


class ExpenseSummary(BaseModel):
    total_amount: float
    total_count: int
    by_category: Dict[str, float]
    monthly_summary: Dict[str, float]