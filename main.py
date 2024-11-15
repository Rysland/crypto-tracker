import logging
import sys
import time
from api.coinmarketcap_api import CoinMarketCapAPI
from api.token_filter import filter_tokens_by_contract
from utils import save_tokens_to_cache, load_tokens_from_cache

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def update_tokens_cache():
    """
    Обновляет токены, запрашивая данные с CoinMarketCap.
    """
    try:
        cmc_api = CoinMarketCapAPI()
        tokens = []

        start = 1
        limit = 100

        while start <= 1000:
            logging.info(f"Запрашиваю токены с {start} по {start + limit - 1}")
            batch = cmc_api.get_top_tokens(start=start, limit=limit)

            if not batch:
                logging.warning("Не удалось получить токены на данном этапе.")
                break

            # Добавляем идентификаторы и платформы токенов
            for token in batch:
                if token is None:  # Проверка на None
                    logging.warning(f"Получен пустой токен: {token}")
                    continue

                token_id = token.get("id")
                name = token.get("name")
                symbol = token.get("symbol")
                platform = token.get("platform", {})
                contract = platform.get("token_address") if platform else None

                # Убедимся, что основные данные существуют
                if not (token_id and name and symbol):
                    logging.warning(f"Пропущен токен из-за отсутствия данных: {token}")
                    continue

                tokens.append({
                    "id": token_id,
                    "name": name,
                    "symbol": symbol,
                    "platform": platform,
                    "contract": contract
                })

            start += limit
            time.sleep(2)  # Задержка для API

        if tokens:
            save_tokens_to_cache(tokens)
            logging.info(f"Токены успешно обновлены. Всего: {len(tokens)}")
        else:
            logging.warning("Не удалось обновить токены.")
    except Exception as e:
        logging.error(f"Ошибка обновления токенов: {e}")

def analyze_tokens():
    """
    Анализирует токены, фильтруя их по контрактам.
    """
    logging.info("Запуск анализа токенов...")
    tokens = load_tokens_from_cache()

    if not tokens:
        logging.error("Токены не найдены. Сначала выполните 'update_tokens'.")
        return

    logging.info(f"Загружено токенов из кэша: {len(tokens)}")
    filtered_tokens = filter_tokens_by_contract(tokens)

    logging.info(f"Отфильтровано токенов: {len(filtered_tokens)}")

    # Здесь можно добавить дополнительные действия с фильтрованными токенами
    for token in filtered_tokens:
        logging.info(f"Токен {token['name']} ({token['symbol']}) контракт: {token['contract']}")

def main():
    """
    Основной запуск программы.
    """
    if len(sys.argv) < 2:
        logging.error("Не указана команда. Используйте 'update_tokens' или 'analyze_tokens'.")
        return

    command = sys.argv[1]

    if command == "update_tokens":
        update_tokens_cache()
    elif command == "analyze_tokens":
        analyze_tokens()
    else:
        logging.error(f"Неизвестная команда: {command}")

if __name__ == "__main__":
    main()
