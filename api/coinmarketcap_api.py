import os
import requests
from dotenv import load_dotenv

# Загружаем API-ключ из .env файла
load_dotenv()
CMC_API_KEY = os.getenv("CMC_API_KEY")

class CoinMarketCapAPI:
    """Класс для взаимодействия с API CoinMarketCap."""

    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        if not CMC_API_KEY:
            raise ValueError("API-ключ CoinMarketCap не найден. Проверьте файл .env")

    def get_top_tokens(self, start=1, limit=100):
        """
        Получает список токенов по капитализации.

        :param start: Начало списка (порядковый номер токена).
        :param limit: Количество токенов для получения.
        :return: Список токенов или пустой список при ошибке.
        """
        url = f"{self.base_url}/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"start": start, "limit": limit, "convert": "USD"}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data["data"] if "data" in data else []
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к CoinMarketCap: {e}")
            return []

    def get_tokens_info(self, ids):
        """
        Получает информацию о токенах по их ID.

        :param ids: Список ID токенов.
        :return: Словарь с информацией о токенах или пустой словарь при ошибке.
        """
        url = f"{self.base_url}/cryptocurrency/info"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"id": ",".join(map(str, ids))}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data["data"] if "data" in data else {}
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к CoinMarketCap: {e}")
            return {}
