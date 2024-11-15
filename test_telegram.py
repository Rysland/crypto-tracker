import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Загрузка переменных из .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def send_test_message():
    """
    Асинхронно отправляет тестовое сообщение в Telegram.
    """
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        message = "Тестовое сообщение от бота."
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info("Сообщение успешно отправлено в Telegram.")
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())
