import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')  # Получаем ключ из .env
BASE_URL = 'https://api.etherscan.io/api'

# Функция для получения баланса эфира на кошельке
def get_balance(address):
    url = f'{BASE_URL}?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Error fetching balance for {address}")
        return None

# Функция для получения баланса токенов на кошельке
def get_token_balance(address, contract_address):
    url = f'{BASE_URL}?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Error fetching token balance for {address}")
        return None

# Функция для получения информации о токене (например, объем поставки)
def get_token_info(contract_address):
    url = f'https://api.etherscan.io/api?module=token&action=getTokenInfo&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':  # Проверяем, что статус ответа успешный
        total_supply = int(data['result']['totalSupply'])
        return total_supply
    return None

# Функция для получения списка держателей токенов
def get_token_holders(contract_address):
    etherscan_api_key = 'your_etherscan_api_key'  # Замените на свой API ключ
    url = f'https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={contract_address}&apikey={etherscan_api_key}'
    
    response = requests.get(url)
    data = response.json()
    return data['result']

# Функция для анализа распределения токенов по кошелькам
def analyze_token_distribution(contract_address, total_supply):
    holders = get_token_holders(contract_address)
    holder_info = []
    
    for holder in holders:
        address = holder['HolderAddress']
        balance = int(holder['TokenQuantity'])
        percentage = (balance / total_supply) * 100  # Считаем процент от общего объема токенов
        holder_info.append({'address': address, 'balance': balance, 'percentage': percentage})
    
    return holder_info

# Функция для анализа концентрации токенов
def check_token_concentration(contract_address, total_supply, threshold=70):
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


