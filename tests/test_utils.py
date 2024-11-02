import logging

import pytest

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

API_KEY = "f98ee1d2c0fbccb39e80f2d528735b0e"


# Фикстура для патчинга запросов к внешним API
@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(url, params):
        if url == "http://api.marketstack.com/v1/eod":
            return MockResponse(
                {
                    "data": [
                        {"symbol": "USD", "close": 134.51},
                        {"symbol": "RUB", "close": 1},
                    ]
                },
                200,
            )
