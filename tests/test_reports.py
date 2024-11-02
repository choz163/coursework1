from datetime import datetime

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


# Фикстура для генерации тестовых данных
@pytest.fixture
def transactions():
    return pd.DataFrame(
        {
            "Дата операции": [
                "2023-03-08",
                "2023-03-09",
                "2023-03-10",
                "2023-03-11",
                "2023-03-12",
            ],
            "Категория": ["Еда", "Развлечения", "Еда", "Транспорт", "Одежда"],
            "Сумма операции": [100, 200, 300, 400, 500],
        }
    )


# Тесты для функции spending_by_category
@pytest.mark.parametrize(
    "category, expected_result",
    [
        ("Еда", {"2023-03-08": 100, "2023-03-10": 300}),
        ("Развлечения", {"2023-03-09": 200}),
        ("Транспорт", {"2023-03-11": 400}),
        ("Одежда", {"2023-03-12": 500}),
    ],
)
def test_spending_by_category(transactions, category, expected_result):
    result = spending_by_category(transactions, category)
    assert result == expected_result


# Тесты для функции spending_by_weekday
@pytest.mark.parametrize(
    "date, expected_result",
    [
        (
            "2023-03-12",
            {
                "Понедельник": 100,
                "Вторник": 200,
                "Среда": 300,
                "Четверг": 400,
                "Пятница": 500,
            },
        ),
        ("2023-03-11", {"Суббота": 400, "Воскресенье": 500}),
    ],
)
def test_spending_by_weekday(transactions, date, expected_result):
    result = spending_by_weekday(transactions, date)
    assert result == expected_result


# Тесты для функции spending_by_workday
@pytest.mark.parametrize(
    "date, expected_result",
    [
        ("2023-03-12", {"Рабочий день": 1000, "Выходной день": 1000}),
        ("2023-03-11", {"Рабочий день": 700, "Выходной день": 900}),
    ],
)
def test_spending_by_workday(transactions, date, expected_result):
    result = spending_by_workday(transactions, date)
    assert result == expected_result
