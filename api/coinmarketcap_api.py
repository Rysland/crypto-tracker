import os
import requests
from dotenv import load_dotenv
import logging

# Загружаем API-ключ из .env файла
load_dotenv()
CMC_API_KEY = os.getenv("CMC_API_KEY")  # Убедитесь, что ключ указан корректно в .env

class CoinMarketCapAPI:
    """Класс для взаимодействия с API CoinMarketCap."""

    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        if not CMC_API_KEY:
            raise ValueError("API-ключ CoinMarketCap не найден. Проверьте файл .env")
        self.headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}

    def get_top_tokens(self, start=1, limit=100):
        """
        Получает список токенов по капитализации.

        :param start: Начало списка (порядковый номер токена)
        :param limit: Количество токенов для получения
        :return: Список токенов
        """
        url = f"{self.base_url}/cryptocurrency/listings/latest"
        params = {"start": start, "limit": limit, "convert": "USD"}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data["data"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка запроса к CoinMarketCap: {e}")
            return []

    def get_token_info(self, ids):
        """
        Получает подробную информацию о токенах по их ID.

        :param ids: Список ID токенов
        :return: Информация о токенах
        """
        url = f"{self.base_url}/cryptocurrency/info"
        params = {"id": ",".join(map(str, ids))}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data["data"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка запроса к CoinMarketCap: {e}")
            return {}
