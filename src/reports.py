import datetime
from typing import Dict, Optional

import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> Dict[str, float]:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    start_date = datetime.datetime.strptime(date, "%Y-%m-%d") - pd.DateOffset(months=3)
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    transactions_in_period = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]
    transactions_in_category = transactions_in_period[
        transactions_in_period["Категория"] == category
    ]

    return (
        transactions_in_category.groupby("Дата операции")["Сумма операции"]
        .sum()
        .to_dict()
    )


def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> Dict[str, float]:
    """Возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    start_date = datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(
        days=90
    )
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    transactions_in_period = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]
    transactions_in_period["День недели"] = transactions_in_period[
        "Дата операции"
    ].dt.day_name()

    return (
        transactions_in_period.groupby("День недели")["Сумма операции"].mean().to_dict()
    )


def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> Dict[str, float]:
    """Возвращает средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    start_date = datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(
        days=90
    )
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    transactions_in_period = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]
    transactions_in_period["День недели"] = transactions_in_period[
        "Дата операции"
    ].dt.day_name()
    transactions_in_period["Рабочий день"] = transactions_in_period["День недели"].isin(
        ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    )

    return (
        transactions_in_period.groupby("Рабочий день")["Сумма операции"]
        .mean()
        .to_dict()
    )
