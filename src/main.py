import json
from src.views import get_main_page_data, get_events_page_data
from src.services import get_profitable_categories, get_investment_bank, get_simple_search
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
import pandas as pd
from pathlib import Path

def main():
    # Загрузка данных из Excel-файла
    data_file_path = Path(__file__).parent.parent / 'data' / 'operations.xlsx'
    transactions = pd.read_excel(data_file_path)
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    # Получение данных для главной страницы
    date_time = '2023-03-08 12:34:56'
    main_page_data = get_main_page_data(date_time, transactions)  # Передаем transactions
    print("Главная страница:")
    print(json.dumps(main_page_data, ensure_ascii=False, indent=4))  # Убедитесь, что выводит кириллицу

    # Получение выгодных категорий
    year = 2023
    month = 3
    profitable_categories = get_profitable_categories(transactions, year, month)  # Передаем transactions, year и month
    print("\nВыгодные категории:")
    print(json.dumps(profitable_categories, ensure_ascii=False, indent=4))

    # Получение данных для страницы событий
    period = 'M'
    events_page_data = get_events_page_data(date_time, transactions, period)  # Передаем transactions
    print("\nСтраница событий:")
    print(json.dumps(events_page_data, ensure_ascii=False, indent=4))

    # Пример использования функции "Инвесткопилка"
    limit = 100  # Установите лимит округления
    investment_amount = get_investment_bank('2023-03', transactions.to_dict('records'), limit)  # Передаем транзакции как список словарей
    print("\nСумма для инвесткопилки:")
    print(investment_amount)

    # Пример простого поиска
    search_query = 'переводы'
    search_results = get_simple_search(search_query)
    print("\nРезультаты простого поиска:")
    print(json.dumps(search_results, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    main()
