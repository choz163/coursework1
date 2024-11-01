import os
import requests
import datetime
import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_KEY = 'f98ee1d2c0fbccb39e80f2d528735b0e'

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Определяем путь к файлу operations.xlsx
data_file_path = Path(__file__).parent.parent / 'data' / 'operations.xlsx'

# Загрузка данных из Excel-файла
transactions = pd.read_excel(data_file_path)
transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')

def get_currency_rates() -> Dict[str, float]:
    """Возвращает словарь с курсами валют."""
    url = f'http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols=USD,RUB'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'Realtime Currency Exchange Rate' in data:
            exchange_rate = data['Realtime Currency Exchange Rate']
            return {
                'USD/RUB': float(exchange_rate['5. Exchange Rate'])
            }
        else:
            logging.error(f"Ошибка получения данных: {data.get('Error Message', 'Неизвестная ошибка')}")
            return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса: {e}")
        return {}
    except ValueError as e:
        logging.error(f"Ошибка декодирования JSON: {e}")
        return {}

def get_profitable_categories(transactions: pd.DataFrame, year: int, month: int) -> Dict[str, float]:
    """Возвращает анализ выгодных категорий для кешбэка."""
    transactions_in_month = transactions[
        (transactions['Дата операции'].dt.year == year) & (transactions['Дата операции'].dt.month == month)]

    categories = transactions_in_month['Категория'].unique()
    profitable_categories = {}
    for category in categories:
        transactions_in_category = transactions_in_month[transactions_in_month['Категория'] == category]
        total_amount = transactions_in_category['Сумма операции'].sum()
        cashback = transactions_in_category['Кэшбэк'].sum()
        profitable_categories[category] = cashback / total_amount * 100 if total_amount else 0

    return profitable_categories

def get_investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    total_investment = 0.0
    month_date = datetime.datetime.strptime(month, '%Y-%m')

    for transaction in transactions:
        transaction_date = transaction['Дата операции']
        if transaction_date.year == month_date.year and transaction_date.month == month_date.month:
            rounded_amount = (transaction['Сумма операции'] // limit + 1) * limit
            total_investment += rounded_amount - transaction['Сумма операции']

    return total_investment

def get_simple_search(query: str) -> List[Dict[str, Any]]:
    """Возвращает список транзакций, содержащих запрос в описании или категории."""
    return transactions[
        (transactions['Описание'].str.contains(query)) | (transactions['Категория'].str.contains(query))].to_dict('records')
