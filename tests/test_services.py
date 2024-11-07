from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import (
    get_card_data,
    get_currency_rates,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
)


@pytest.fixture
def transactions():
    """Фикстура для генерации тестовых данных."""
    return pd.DataFrame(
        {
            "Номер карты": ["1111222233334444", "5555666677778888", "1111222233334444"],
            "Сумма операции": [100, 200, 300],
            "Кэшбэк": [10, 20, 30],
            "Дата операции": pd.to_datetime(["2023-03-08", "2023-03-09", "2023-03-08"]),
        }
    )


# Тесты для функции get_currency_rates
@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {
        "data": [{"symbol": "USD", "close": 134.51}, {"symbol": "RUB", "close": 1}]
    }
    rates = get_currency_rates()
    assert rates == {"USD": 134.51, "RUB": 1}


# Тесты для функции get_stock_prices
@patch("requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = {
        "data": [
            {"symbol": "AAPL", "close": 150.00},
            {"symbol": "AMZN", "close": 2000.00},
        ]
    }
    prices = get_stock_prices(["AAPL", "AMZN"])
    assert prices == {"AAPL": 150.00, "AMZN": 2000.00}


# Тесты для функции get_greeting
@pytest.mark.parametrize(
    "current_time, expected_result",
    [
        (pd.Timestamp("2023-03-08 05:00:00"), "Доброй ночи"),
        (pd.Timestamp("2023-03-08 10:00:00"), "Доброе утро"),
        (pd.Timestamp("2023-03-08 15:00:00"), "Добрый день"),
        (pd.Timestamp("2023-03-08 20:00:00"), "Добрый вечер"),
    ],
)
def test_get_greeting(current_time, expected_result):
    result = get_greeting(current_time)
    assert result == expected_result


# Тесты для функции get_card_data
def test_get_card_data(transactions):
    card_data = get_card_data(transactions)
    assert card_data == [
        {"last_digits": "4444", "total_spent": 400, "cashback": 40},
        {"last_digits": "8888", "total_spent": 200, "cashback": 20},
    ]


# Тесты для функции get_top_transactions
def test_get_top_transactions(transactions):
    top_transactions = get_top_transactions(transactions)
    assert top_transactions == [
        {"Дата операции": pd.Timestamp("2023-03-08"), "Сумма операции": 300},
        {"Дата операции": pd.Timestamp("2023-03-09"), "Сумма операции": 200},
        {"Дата операции": pd.Timestamp("2023-03-08"), "Сумма операции": 100},
    ]
