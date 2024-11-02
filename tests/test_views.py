import datetime
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import pytest
from dotenv import load_dotenv

from src.utils import (
    get_card_data,
    get_currency_rates,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
)
from src.views import get_events_page_data, get_main_page_data

# Загружаем переменные окружения
load_dotenv()

# Определяем путь к файлу operations.xlsx
data_file_path = Path(__file__).parent.parent / "data" / "operations.xlsx"

# Загрузка данных из Excel-файла
transactions = pd.read_excel(data_file_path)
transactions["Дата операции"] = pd.to_datetime(
    transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
)


# Фикстура для генерации тестовых данных
@pytest.fixture
def test_data():
    return {"date_time": "2023-03-08 12:34:56", "transactions": transactions}


# Тесты для функции get_main_page_data
@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        (
            {"date_time": "2023-03-08 12:34:56", "transactions": transactions},
            {
                "greeting": "Добрый день",
                "cards": [],
                "top_transactions": [],
                "currency_rates": {},
                "stock_prices": {},
            },
        )
    ],
)
def test_get_main_page_data(test_data, expected_result):
    result = get_main_page_data(**test_data)
    assert result == expected_result


# Тесты для функции get_events_page_data
@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        (
            {"date_time": "2023-03-08 12:34:56", "transactions": transactions},
            {"expenses": {}, "income": {}, "currency_rates": {}, "stock_prices": {}},
        )
    ],
)
def test_get_events_page_data(test_data, expected_result):
    result = get_events_page_data(**test_data)
    assert result == expected_result
