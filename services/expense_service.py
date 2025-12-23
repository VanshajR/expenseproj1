from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd

from constants import CATEGORIES, PAYMENT_METHODS
from db.database import execute, fetch_all


class ExpenseService:
    @staticmethod
    def add_expense(data: Dict[str, Any]) -> int:
        return execute(
            "INSERT INTO expenses(date, amount, category, payment_method, notes) VALUES (?, ?, ?, ?, ?)",
            (
                data["date"],
                float(data["amount"]),
                data["category"],
                data["payment_method"],
                data.get("notes", ""),
            ),
        )

    @staticmethod
    def update_expense(expense_id: int, data: Dict[str, Any]) -> None:
        execute(
            "UPDATE expenses SET date=?, amount=?, category=?, payment_method=?, notes=? WHERE id=?",
            (
                data["date"],
                float(data["amount"]),
                data["category"],
                data["payment_method"],
                data.get("notes", ""),
                expense_id,
            ),
        )

    @staticmethod
    def delete_expense(expense_id: int) -> None:
        execute("DELETE FROM expenses WHERE id=?", (expense_id,))

    @staticmethod
    def list_expenses() -> pd.DataFrame:
        rows = fetch_all("SELECT * FROM expenses ORDER BY date DESC")
        return pd.DataFrame(rows, columns=rows[0].keys() if rows else [])

    @staticmethod
    def get_expense(expense_id: int) -> Optional[Dict[str, Any]]:
        rows = fetch_all("SELECT * FROM expenses WHERE id=?", (expense_id,))
        if not rows:
            return None
        row = rows[0]
        return dict(row)

    @staticmethod
    def seed_sample_data() -> None:
        if fetch_all("SELECT COUNT(*) as cnt FROM expenses")[0]["cnt"] > 0:
            return
        start_date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
        end_date = datetime.today().date()
        categories = CATEGORIES
        payments = PAYMENT_METHODS

        dates = pd.date_range(start=start_date, end=end_date, periods=100)
        for i, day in enumerate(dates):
            category = categories[i % len(categories)]
            payment = payments[i % len(payments)]
            # Scaled for INR-like spends
            amount = round(300 + (i % 9) * 120 + (i % 5) * 40 + (i % 7) * 25 + (i % 3) * 15, 2)
            note = f"Auto-sample #{i+1} for {category.lower()}"
            ExpenseService.add_expense(
                {
                    "date": str(day.date()),
                    "amount": amount,
                    "category": category,
                    "payment_method": payment,
                    "notes": note,
                }
            )
