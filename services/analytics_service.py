from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st

from db.database import fetch_all

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


class AnalyticsService:
    @staticmethod
    def _load_dataframe() -> pd.DataFrame:
        rows = fetch_all("SELECT * FROM expenses")
        df = pd.DataFrame(rows, columns=rows[0].keys() if rows else [])
        if df.empty:
            return df
        df["date"] = pd.to_datetime(df["date"])
        return df

    @staticmethod
    def monthly_summary(month: str) -> pd.DataFrame:
        df = AnalyticsService._load_dataframe()
        if df.empty:
            return df
        month_dt = pd.to_datetime(month + "-01")
        filtered = df[df["date"].dt.to_period("M") == month_dt.to_period("M")]
        return filtered

    @staticmethod
    @st.cache_data
    def category_distribution(df: pd.DataFrame) -> Tuple[plt.Figure, pd.Series]:
        if df.empty:
            return plt.figure(), pd.Series(dtype=float)
        breakdown = df.groupby("category")["amount"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        breakdown.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax)
        ax.set_ylabel("")
        ax.set_title("Category Distribution")
        fig.tight_layout()
        fig.savefig(PLOTS_DIR / "category_distribution.png", dpi=200)
        return fig, breakdown

    @staticmethod
    @st.cache_data
    def daily_trend(df: pd.DataFrame):
        if df.empty:
            return plt.figure(), None
        trend = df.groupby("date")["amount"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(trend["date"], trend["amount"], marker="o")
        ax.set_title("Daily Spending Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.grid(True, linestyle="--", alpha=0.5)
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(PLOTS_DIR / "daily_trend.png", dpi=200)
        plotly_fig = px.line(trend, x="date", y="amount", title="Daily Spending Trend")
        return fig, plotly_fig

    @staticmethod
    @st.cache_data
    def monthly_comparison(df: pd.DataFrame):
        if df.empty:
            return plt.figure(), None
        monthly = (
            df.assign(month=df["date"].dt.to_period("M"))
            .groupby("month")["amount"]
            .sum()
            .reset_index()
        )
        monthly["month"] = monthly["month"].astype(str)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(monthly["month"], monthly["amount"], color="#4C72B0")
        ax.set_title("Month-wise Spend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.tick_params(axis="x", rotation=45, labelsize=9)

        if len(monthly) <= 12:
            for rect, val in zip(bars, monthly["amount"]):
                ax.text(rect.get_x() + rect.get_width() / 2, val + max(monthly["amount"]) * 0.01, f"{val:,.0f}", ha="center", va="bottom", fontsize=8)

        fig.tight_layout()
        fig.savefig(PLOTS_DIR / "monthly_comparison.png", dpi=200)

        plotly_fig = px.bar(monthly, x="month", y="amount", title="Month-wise Spend")
        plotly_fig.update_layout(xaxis_tickangle=-45, bargap=0.2)
        if len(monthly) > 12:
            plotly_fig.update_traces(text=None)
        else:
            plotly_fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
        return fig, plotly_fig

    @staticmethod
    def export_custom_range(start_date: str, end_date: str) -> pd.DataFrame:
        df = AnalyticsService._load_dataframe()
        if df.empty:
            return df
        mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))
        return df.loc[mask]
