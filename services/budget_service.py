from typing import Dict, Optional

import pandas as pd

from db.database import execute, fetch_all


class BudgetService:
    DEFAULT_ALERT_THRESHOLD = 0.8

    @staticmethod
    def set_budget(month: str, budget: float, savings_goal: float) -> None:
        execute(
            "INSERT INTO budgets(month, budget, savings_goal) VALUES (?, ?, ?) ON CONFLICT(month) DO UPDATE SET budget=excluded.budget, savings_goal=excluded.savings_goal",
            (month, budget, savings_goal),
        )

    @staticmethod
    def get_budget(month: str) -> Optional[dict]:
        rows = fetch_all("SELECT * FROM budgets WHERE month=?", (month,))
        if not rows:
            return None
        return dict(rows[0])

    @staticmethod
    def save_setting(key: str, value: str) -> None:
        execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    @staticmethod
    def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
        rows = fetch_all("SELECT value FROM settings WHERE key=?", (key,))
        if not rows:
            return default
        return rows[0]["value"]

    @staticmethod
    def spending_alert(spent: float, budget: float) -> Optional[str]:
        if budget <= 0:
            return None
        threshold = float(BudgetService.get_setting("alert_threshold", str(BudgetService.DEFAULT_ALERT_THRESHOLD)))
        if spent >= budget * threshold:
            pct = spent / budget * 100
            return f"Alert: You have used {pct:.1f}% of your budget for the month."
        return None

    @staticmethod
    def monthly_progress(df: pd.DataFrame, month: str) -> Dict[str, float]:
        if df.empty:
            return {"spent": 0.0, "budget": 0.0, "savings_goal": 0.0, "remaining": 0.0}
        target_month = pd.to_datetime(month + "-01").to_period("M")
        filtered = df[df["date"].dt.to_period("M") == target_month]
        spent = filtered["amount"].sum() if not filtered.empty else 0.0
        budget_entry = BudgetService.get_budget(month)
        budget = budget_entry.get("budget", 0.0) if budget_entry else 0.0
        savings_goal = budget_entry.get("savings_goal", 0.0) if budget_entry else 0.0
        remaining = max(budget - spent, 0.0)
        return {
            "spent": spent,
            "budget": budget,
            "savings_goal": savings_goal,
            "remaining": remaining,
        }
