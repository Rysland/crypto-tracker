import requests
import os
from dotenv import load_dotenv

# ��������� ���������� ��������� �� ����� .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')  # �������� ���� �� .env
BASE_URL = 'https://api.etherscan.io/api'

# ������� ��� ��������� ������� ����� �� ��������
def get_balance(address):
    url = f'{BASE_URL}?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # ���������� ������ � ������� JSON
    else:
        print(f"Error fetching balance for {address}")
        return None

# ������� ��� ��������� ������� ������� �� ��������
def get_token_balance(address, contract_address):
    url = f'{BASE_URL}?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # ���������� ������ � ������� JSON
    else:
        print(f"Error fetching token balance for {address}")
        return None

# ������� ��� ��������� ���������� � ������ (��������, ����� ��������)
def get_token_info(contract_address):
    url = f'https://api.etherscan.io/api?module=token&action=getTokenInfo&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':  # ���������, ��� ������ ������ ��������
        total_supply = int(data['result']['totalSupply'])
        return total_supply
    return None

# ������� ��� ��������� ������ ���������� �������
def get_token_holders(contract_address):
    etherscan_api_key = 'your_etherscan_api_key'  # �������� �� ���� API ����
    url = f'https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={contract_address}&apikey={etherscan_api_key}'
    
    response = requests.get(url)
    data = response.json()
    return data['result']

# ������� ��� ������� ������������� ������� �� ���������
def analyze_token_distribution(contract_address, total_supply):
    holders = get_token_holders(contract_address)
    holder_info = []
    
    for holder in holders:
        address = holder['HolderAddress']
        balance = int(holder['TokenQuantity'])
        percentage = (balance / total_supply) * 100  # ������� ������� �� ������ ������ �������
        holder_info.append({'address': address, 'balance': balance, 'percentage': percentage})
    
    return holder_info

# ������� ��� ������� ������������ �������
def check_token_concentration(contract_address, total_supply, threshold=70):
    holder_info = analyze_token_distribution(contract_address, total_supply)
    
    high_concentration = []
    for holder in holder_info:
        if holder['percentage'] > threshold:  # ���� ������� ������ ������ 70% �� ������ ������
            high_concentration.append(holder)
    
    if high_concentration:
        # ��������� ��������� ��� Telegram
        message = f"Token {contract_address} has high concentration:\n"
        for holder in high_concentration:
            message += f"Address: {holder['address']}, Balance: {holder['balance']}, Percentage: {holder['percentage']}%\n"
        send_telegram_message(message)


