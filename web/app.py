from flask import Flask, render_template
from api.etherscan import get_transactions, get_balance, get_token_balance, get_token_info, get_token_holders, analyze_token_distribution, check_token_concentration, send_telegram_message
from pycoingecko import CoinGeckoAPI
import requests
import os
from dotenv import load_dotenv
from telegram import Bot

# Инициализируем Flask-приложение
app = Flask(__name__)

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен и chat_id из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Инициализируем CoinGecko API для получения данных о капитализации
cg = CoinGeckoAPI()

# Функции для работы с Etherscan API

def get_transactions(address):
    """Получаем список транзакций для указанного кошелька."""
    etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')  # Получаем ключ API из .env
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={etherscan_api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Error fetching transactions for {address}")
        return None

def get_balance(address):
    """Получаем баланс эфира на кошельке."""
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={os.getenv("ETHERSCAN_API_KEY")}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Error fetching balance for {address}")
        return None

def get_token_balance(address, contract_address):
    """Получаем баланс токенов на кошельке для указанного контракта."""
    url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={os.getenv("ETHERSCAN_API_KEY")}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Error fetching token balance for {address}")
        return None

def get_token_info(contract_address):
    """Получаем общую информацию о токене, включая объем поставки."""
    url = f'https://api.etherscan.io/api?module=token&action=getTokenInfo&contractaddress={contract_address}&apikey={os.getenv("ETHERSCAN_API_KEY")}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':  # Проверяем, что статус ответа успешный
        total_supply = int(data['result']['totalSupply'])
        return total_supply
    return None

def get_token_holders(contract_address):
    """Получаем список держателей токенов для контракта."""
    url = f'https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={contract_address}&apikey={os.getenv("ETHERSCAN_API_KEY")}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def analyze_token_distribution(contract_address, total_supply):
    """Анализируем распределение токенов по кошелькам."""
    holders = get_token_holders(contract_address)
    holder_info = []
    
    for holder in holders:
        address = holder['HolderAddress']
        balance = int(holder['TokenQuantity'])
        percentage = (balance / total_supply) * 100  # Считаем процент от общего объема токенов
        holder_info.append({'address': address, 'balance': balance, 'percentage': percentage})
    
    return holder_info

def check_token_concentration(contract_address, total_supply, threshold=70):
    """Проверяем концентрацию токенов на нескольких кошельках."""
    holder_info = analyze_token_distribution(contract_address, total_supply)
    
    high_concentration = []
    for holder in holder_info:
        if holder['percentage'] > threshold:  # Если кошелек держит больше 70% от общего объема
            high_concentration.append(holder)
    
    if high_concentration:
        # Генерация сообщения для Telegram
        message = f"Token {contract_address} has high concentration:\n"
        for holder in high_concentration:
            message += f"Address: {holder['address']}, Balance: {holder['balance']}, Percentage: {holder['percentage']}%\n"
        send_telegram_message(message)

# Функция для отправки сообщений в Telegram
def send_telegram_message(message):
    """Отправка сообщения в Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)  # Инициализация бота с токеном
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)  # Отправка сообщения в чат

# Получаем список токенов с капитализацией через CoinGecko API
def get_tokens_by_market_cap():
    """Получаем топ 100 токенов по капитализации."""
    tokens = cg.get_coins_markets(vs_currency='usd')
    return tokens

@app.route('/')
def home():
    """Основная страница для обработки токенов."""
    tokens = get_tokens_by_market_cap()  # Получаем список токенов с капитализацией

    # Для каждого токена проверяем информацию о капитализации, держателях и концентрации
    for token in tokens[:10]:  # Ограничиваем до 10 токенов для теста
        contract_address = token['id']  # Предполагаем, что 'id' - это контракт токена
        total_supply = get_token_info(contract_address)

        if total_supply:
            # Проверяем концентрацию токенов
            check_token_concentration(contract_address, total_supply)

    return render_template('index.html')

# Запуск Flask приложения
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

