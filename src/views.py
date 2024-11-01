import json
import requests
import datetime
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from src.utils import get_currency_rates, get_stock_prices, get_greeting, get_card_data, get_top_transactions

# Определяем путь к файлу operations.xlsx
data_file_path = Path(__file__).parent.parent / 'data' / 'operations.xlsx'

# Загрузка данных из Excel-файла
transactions = pd.read_excel(data_file_path)

# Преобразуем столбец "Дата операции" в формат datetime
transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')


# Функция для получения JSON-ответа для главной страницы
def get_main_page_data(date_time: str, transactions: pd.DataFrame) -> Dict[str, Any]:
    """Возвращает JSON-ответ для главной страницы."""

    current_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    greeting = get_greeting(current_time)
    card_data = get_card_data(transactions)
    top_transactions = get_top_transactions(transactions)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices(['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA'])  # Передаем символы акций

    # Преобразуем временные метки в строки для сериализации
    for transaction in top_transactions:
        transaction['Дата операции'] = transaction['Дата операции'].strftime('%Y-%m-%d %H:%M:%S')

    return {
        'greeting': greeting,
        'cards': card_data,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }


# Функция для получения JSON-ответа для страницы событий
def get_events_page_data(date_time: str, transactions: pd.DataFrame, period: str = 'M') -> Dict[str, Any]:
    """Возвращает JSON-ответ для страницы событий."""

    current_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    if period == 'W':
        start_date = current_time - datetime.timedelta(days=current_time.weekday())
        end_date = start_date + datetime.timedelta(days=6)
    elif period == 'M':
        start_date = current_time.replace(day=1)
        end_date = current_time
    elif period == 'Y':
        start_date = current_time.replace(month=1, day=1)
        end_date = current_time
    elif period == 'ALL':
        start_date = transactions['Дата операции'].min()
        end_date = current_time
    else:
        raise ValueError('Неверный период')

    transactions_in_period = transactions[
        (transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= end_date)]
    expenses = transactions_in_period[transactions_in_period['Сумма операции'] < 0]
    income = transactions_in_period[transactions_in_period['Сумма операции'] > 0]

    expenses_by_category = expenses.groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False).head(
        7).to_dict()
    expenses_by_category['Остальное'] = expenses.groupby('Категория')['Сумма операции'].sum().sort_values(
        ascending=False).tail().sum()

    return {
        'expenses': expenses_by_category,
        'income': income.groupby('Категория')['Сумма операции'].sum().to_dict(),
        'currency_rates': get_currency_rates(),
        'stock_prices': get_stock_prices(['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']),  # Передаем символы акций
    }
