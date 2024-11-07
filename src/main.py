import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from src.services import (
    get_investment_bank,
    get_profitable_categories,
    get_simple_search,
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

# Получение данных для главной страницы
date_time = "2023-03-08 12:34:56"
main_page_data = get_main_page_data(date_time, transactions)
print("Главная страница:")
print(json.dumps(main_page_data, ensure_ascii=False, indent=4))

# Получение выгодных категорий
year = 2023
month = 3
profitable_categories = get_profitable_categories(transactions, year, month)
print("\nВыгодные категории:")
print(json.dumps(profitable_categories, ensure_ascii=False, indent=4))

# Получение данных для страницы событий
period = "M"
events_page_data = get_events_page_data(date_time, transactions, period)
print("\nСтраница событий:")
print(json.dumps(events_page_data, ensure_ascii=False, indent=4))

# Пример использования функции "Инвесткопилка"
limit = 100
investment_amount = get_investment_bank(
    "2023-03", transactions.to_dict("records"), limit
)
print("\nСумма для инвесткопилки:")
print(investment_amount)

# Пример простого поиска
search_query = "переводы"
search_results = get_simple_search(search_query)
print("\nРезультаты простого поиска:")
print(json.dumps(search_results, ensure_ascii=False, indent=4))
