import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
BASE_URL = 'https://api.etherscan.io/api'

def get_transactions(address):
    url = f'{BASE_URL}?module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print("Error fetching data from Etherscan")
        return None

# Пример использования
if __name__ == "__main__":
    address = '0x8bC43A1810a178FB28e91bCa06D437C74df33250'  # Замените на адрес Ethereum-кошелька
    data = get_transactions(address)
    if data:
        print(data)
