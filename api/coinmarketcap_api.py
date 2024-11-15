import os
import requests
from dotenv import load_dotenv

# Загружаем API-ключ из .env файла
load_dotenv()
CMC_API_KEY = os.getenv("CMC_API_KEY")  # Убедитесь, что ключ указан корректно в .env

class CoinMarketCapAPI:
    """Класс для взаимодействия с API CoinMarketCap."""

    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        if not CMC_API_KEY:
            raise ValueError("API-ключ CoinMarketCap не найден. Проверьте файл .env")

    def get_top_tokens(self, start=1, limit=1000):
        """
        Получает список токенов по капитализации.

        :param start: Начало списка (порядковый номер токена)
        :param limit: Количество токенов для получения
        :return: Список токенов или пустой список при ошибке
        """
        url = f"{self.base_url}/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"start": start, "limit": limit, "convert": "USD"}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                return data["data"]
            else:
                raise ValueError(f"Некорректный ответ API: {data}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к CoinMarketCap: {e}")
        except ValueError as e:
            print(f"Ошибка в данных CoinMarketCap: {e}")
        return []

    def get_token_info(self, symbol):
        """
        Получает информацию о токене по его символу.

        :param symbol: Символ токена (например, ETH)
        :return: Информация о токене или пустой словарь при ошибке
        """
        url = f"{self.base_url}/cryptocurrency/info"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"symbol": symbol}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "data" in data and symbol.upper() in data["data"]:
                return data["data"][symbol.upper()]
            else:
                raise ValueError(f"Информация о токене '{symbol}' отсутствует в ответе API: {data}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к CoinMarketCap: {e}")
        except ValueError as e:
            print(f"Ошибка в данных CoinMarketCap: {e}")
        return {}
