import logging
import sys
import time
import os
import asyncio
from dotenv import load_dotenv
from api.coinmarketcap_api import CoinMarketCapAPI
from api.token_filter import filter_tokens_by_contract
from utils import save_tokens_to_cache, load_tokens_from_cache
from telegram import Bot

# Загрузка переменных из .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def send_telegram_message(bot_token, chat_id, message):
    """
    Отправляет сообщение в Telegram.
    """
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
        logging.info("Сообщение отправлено в Telegram.")
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения в Telegram: {e}")

async def filter_and_notify(tokens):
    """
    Фильтрует токены по заданным условиям и отправляет уведомления в Telegram.
    """
    logging.info("Начинаю фильтрацию токенов для уведомлений.")
    interesting_tokens = []

    for token in tokens:
        # Пример фильтрации: токены с контрактами и определёнными условиями
        contract = token.get("contract")
        if not contract:
            continue

        # Условия для определения "интересных" токенов (замените на ваши критерии)
        if token['platform']['name'] == 'Ethereum' and token['symbol'].startswith('A'):
            interesting_tokens.append(token)

    logging.info(f"Найдено интересных токенов: {len(interesting_tokens)}")

    # Отправка уведомлений с задержкой
    for token in interesting_tokens:
        message = (
            f"Найден интересный токен:\n"
            f"Название: {token['name']}\n"
            f"Символ: {token['symbol']}\n"
            f"Контракт: {token['contract']}\n"
            f"Платформа: {token['platform']['name']}"
        )
        await send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
        await asyncio.sleep(2)  # Задержка в 2 секунды между сообщениями

async def analyze_tokens():
    """
    Анализирует токены, фильтруя их по контрактам и отправляя уведомления.
    """
    logging.info("Запуск анализа токенов...")
    tokens = load_tokens_from_cache()

    if not tokens:
        logging.error("Токены не найдены. Сначала выполните 'update_tokens'.")
        return

    logging.info(f"Загружено токенов из кэша: {len(tokens)}")
    await filter_and_notify(tokens)

async def update_tokens_cache():
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

            for token in batch:
                if token is None:
                    logging.warning(f"Получен пустой токен: {token}")
                    continue

                token_id = token.get("id")
                name = token.get("name")
                symbol = token.get("symbol")
                platform = token.get("platform", {})
                contract = platform.get("token_address") if platform else None

                if not (token_id and name and symbol):
                    logging.warning(f"Пропущен токен из-за отсутствия данных: {token}")
                    continue

                if not platform:
                    logging.debug(f"Токен {name} ({symbol}) не имеет привязки к платформе.")
                    continue

                tokens.append({
                    "id": token_id,
                    "name": name,
                    "symbol": symbol,
                    "platform": platform,
                    "contract": contract
                })

            start += limit
            time.sleep(2)

        if tokens:
            save_tokens_to_cache(tokens)
            logging.info(f"Токены успешно обновлены. Всего: {len(tokens)}")
        else:
            logging.warning("Не удалось обновить токены.")
    except Exception as e:
        logging.error(f"Ошибка обновления токенов: {e}")

async def main():
    """
    Основной запуск программы.
    """
    if len(sys.argv) < 2:
        logging.error("Не указана команда. Используйте 'update_tokens' или 'analyze_tokens'.")
        return

    command = sys.argv[1]

    if command == "update_tokens":
        await update_tokens_cache()
    elif command == "analyze_tokens":
        await analyze_tokens()
    else:
        logging.error(f"Неизвестная команда: {command}")

if __name__ == "__main__":
    asyncio.run(main())
