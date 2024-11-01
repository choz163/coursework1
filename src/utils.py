import datetime
import logging
import pandas as pd  # Импортируем pandas
from typing import List, Dict, Any
import requests  # Импортируем requests для работы с API

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = 'f98ee1d2c0fbccb39e80f2d528735b0e'

def get_currency_rates() -> Dict[str, float]:
    """Возвращает словарь с курсами валют."""
    url = f'http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols=USD,RUB'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный ответ
        data = response.json()

        # Проверяем наличие данных
        if 'data' in data and len(data['data']) > 0:
            rates = {}
            for rate in data['data']:
                rates[rate['symbol']] = rate['close']  # Получаем цену закрытия
            return rates
        else:
            logging.error(f"Ошибка получения данных: {data.get('error', 'Неизвестная ошибка')}")
            return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса: {e}")
        return {}
    except ValueError as e:
        logging.error(f"Ошибка декодирования JSON: {e}")
        return {}


def get_stock_prices(symbols: List[str]) -> Dict[str, float]:
    """Возвращает словарь с ценами на акции."""
    prices = {}
    for symbol in symbols:
        url = f'http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={symbol}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на успешный ответ
            data = response.json()

            # Проверяем наличие данных
            if 'data' in data and len(data['data']) > 0:
                last_data = data['data'][0]  # Берем последнюю запись
                prices[symbol] = last_data['close']  # Получаем цену закрытия
            else:
                logging.error(f"Ошибка получения данных для {symbol}: {data.get('error', 'Неизвестная ошибка')}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка запроса: {e}")
        except ValueError as e:
            logging.error(f"Ошибка декодирования JSON: {e}")

    return prices


def get_greeting(current_time: datetime.datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if hour < 6:
        return 'Доброй ночи'
    elif hour < 12:
        return 'Доброе утро'
    elif hour < 18:
        return 'Добрый день'
    else:
        return 'Добрый вечер'


def get_card_data(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает список словарей с данными о картах."""
    cards = transactions['Номер карты'].unique()
    card_data = []
    for card in cards:
        card_data.append({
            'last_digits': float(str(card[-4:])),
            'total_spent': transactions[transactions['Номер карты'] == card]['Сумма операции'].sum(),
            'cashback': transactions[transactions['Номер карты'] == card]['Кэшбэк'].sum()
        })
    return card_data


def get_top_transactions(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает список словарей с топ-5 транзакциями."""
    return transactions.sort_values('Сумма платежа', ascending=False).head(5).to_dict('records')
