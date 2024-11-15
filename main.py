import json
import logging
import sys
import time
from api.token_filter import filter_tokens_by_blockchain
from api.coinmarketcap_api import CoinMarketCapAPI
from api.blockchain_api import BlockchainAPI
from api.notifications import notify_about_token

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CACHE_FILE = "tokens_cache.json"

def load_tokens_from_cache():
    """
    Загружает токены из локального кэша.
    :return: Список токенов.
    """
    try:
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Файл кэша не найден. Выполните обновление с помощью команды 'update_tokens'.")
        return []
    except json.JSONDecodeError:
        logging.error("Ошибка чтения файла кэша. Выполните обновление с помощью команды 'update_tokens'.")
        return []

def update_tokens_cache():
    """
    Обновляет кэш токенов с CoinMarketCap.
    """
    try:
        cmc_api = CoinMarketCapAPI()
        tokens = []

        # Пошаговая загрузка по 100 токенов
        start = 1
        limit = 100
        while start <= 1000:
            logging.info(f"Запрашиваю токены с {start} по {start + limit - 1}")
            batch = cmc_api.get_top_tokens(start=start, limit=limit)
            if not batch:
                logging.error("Ошибка получения данных от CoinMarketCap.")
                break
            tokens.extend(batch)
            start += limit
            time.sleep(2)  # Задержка между запросами

        if not tokens:
            logging.error("Не удалось получить токены с CoinMarketCap. Проверьте API-ключ и соединение.")
            return

        with open(CACHE_FILE, "w") as file:
            json.dump(tokens, file, indent=4)
        logging.info(f"Успешно обновлено токенов: {len(tokens)}")

    except Exception as e:
        logging.error(f"Ошибка при обновлении кэша токенов: {e}")

def analyze_holders(contract, blockchain):
    """
    Анализ холдеров токена.
    :param contract: Адрес контракта токена.
    :param blockchain: Название блокчейна.
    :return: Список холдеров с их процентами владения.
    """
    try:
        blockchain_api = BlockchainAPI(blockchain)
        holders = blockchain_api.get_holders(contract)
        return holders
    except Exception as e:
        logging.error(f"Ошибка анализа холдеров для токена {contract} в блокчейне {blockchain}: {e}")
        return None

def main():
    """
    Основная логика анализа токенов.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "update_tokens":
        logging.info("Обновление токенов...")
        update_tokens_cache()
        return

    logging.info("Запуск программы...")

    # Загрузка токенов из кэша
    tokens = load_tokens_from_cache()
    if not tokens:
        logging.error("Токены не найдены. Выполните обновление с помощью команды 'update_tokens'.")
        return

    logging.info(f"Загружено токенов из кэша: {len(tokens)}")
    filtered_tokens = filter_tokens_by_blockchain(tokens)
    if not filtered_tokens:
        logging.error("Фильтрация токенов не дала результатов. Проверьте список поддерживаемых блокчейнов.")
        return

    logging.info(f"Отфильтровано токенов для анализа: {len(filtered_tokens)}")

    for token in filtered_tokens:
        logging.info(f"Анализ токена: {token['name']} ({token['contract']}) на блокчейне {token['blockchain']}")

        holders = analyze_holders(token["contract"], token["blockchain"])
        if not holders:
            logging.warning(f"Холдеры не найдены для токена {token['name']}")
            continue

        # Анализ концентрации
        percentages = [holder["percentage"] for holder in holders]
        percentages.sort(reverse=True)

        if sum(percentages[:10]) > 50:
            notify_about_token(
                token["name"], token["contract"], token["blockchain"], holders[:10], "ОЧЕНЬ ВАЖНЫЙ"
            )
        elif sum(percentages[:100]) > 50:
            notify_about_token(
                token["name"], token["contract"], token["blockchain"], holders[:100], "ВАЖНЫЙ"
            )
        elif sum(percentages[:1000]) > 40:
            notify_about_token(
                token["name"], token["contract"], token["blockchain"], holders[:1000], "НОРМ"
            )

    logging.info("Анализ завершён.")

if __name__ == "__main__":
    main()

