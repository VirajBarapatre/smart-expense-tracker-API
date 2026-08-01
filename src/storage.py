import json
import os
from typing import Dict, List, Optional
from uuid import UUID
from src.models import Expense, ExpenseCreate, ExpenseSummary


class ExpenseStorage:

    def __init__(self, filepath: Optional[str] = "expenses.json"):
        self.filepath = filepath
        self.expenses: Dict[UUID, Expense] = {}
        self.load_from_file()

    def load_from_file(self) -> None:
        if self.filepath and os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    for item in data:
                        expense = Expense(**item)
                        self.expenses[expense.id] = expense
            except (json.JSONDecodeError, ValueError):
                self.expenses = {}

    def save_to_file(self) -> None:
        if self.filepath:
            with open(self.filepath, "w") as f:
                json.dump(
                    [
                        json.loads(exp.model_dump_json())
                        for exp in self.expenses.values()
                    ],
                    f,
                    indent=2,
                )

    def add_expense(self, expense_in: ExpenseCreate) -> Expense:
        expense = Expense(**expense_in.model_dump())
        self.expenses[expense.id] = expense
        self.save_to_file()
        return expense

    def get_all(self, category: Optional[str] = None) -> List[Expense]:
        expenses = list(self.expenses.values())
        if category:
            expenses = [
                e for e in expenses if e.category.lower() == category.lower()
            ]
        return sorted(expenses, key=lambda e: e.date, reverse=True)

    def delete_expense(self, expense_id: UUID) -> bool:
        if expense_id in self.expenses:
            del self.expenses[expense_id]
            self.save_to_file()
            return True
        return False

    def get_summary(self) -> ExpenseSummary:
        total_amount = 0.0
        by_category: Dict[str, float] = {}
        monthly_summary: Dict[str, float] = {}

        for exp in self.expenses.values():
            total_amount += exp.amount

            # Category calculation
            cat_key = exp.category.capitalize()
            by_category[cat_key] = (
                round(by_category.get(cat_key, 0.0) + exp.amount, 2)
            )

            # Monthly summary calculation (YYYY-MM)
            month_key = exp.date.strftime("%Y-%m")
            monthly_summary[month_key] = (
                round(monthly_summary.get(month_key, 0.0) + exp.amount, 2)
            )

        return ExpenseSummary(
            total_amount=round(total_amount, 2),
            total_count=len(self.expenses),
            by_category=by_category,
            monthly_summary=monthly_summary,
        )