import os
from dotenv import load_dotenv
from telegram import Bot

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен и chat_id из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    """Отправка сообщения в Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)  # Инициализация бота с токеном
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)  # Отправка сообщения в чат
