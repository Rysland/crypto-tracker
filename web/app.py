from flask import Flask, jsonify, render_template
from api.blockchain_api import BlockchainAPI
from api.telegram_bot import send_telegram_message
from pycoingecko import CoinGeckoAPI

# Инициализируем Flask-приложение
app = Flask(__name__)

# Инициализируем CoinGecko API для получения данных о капитализации
cg = CoinGeckoAPI()

# Функция для получения списка токенов с капитализацией через CoinGecko API
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
        contract_address = token.get('id')  # Используем 'id' как контракт токена
        blockchain_api = BlockchainAPI("ethereum")  # Пример: Используем эндпоинт Ethereum
        total_supply = blockchain_api.send_request("eth_getTotalSupply", [contract_address])

        if total_supply:
            # Проверяем концентрацию токенов
            check_token_concentration(contract_address, total_supply)

    return render_template('index.html')

@app.route('/test/<blockchain>', methods=['GET'])
def test_blockchain(blockchain):
    """Маршрут для тестирования работы с блокчейнами."""
    api = BlockchainAPI(blockchain)
    result = api.send_request("eth_blockNumber", [])
    if result:
        return jsonify({"blockchain": blockchain, "block_number": result})
    return jsonify({"error": f"Не удалось получить данные для блокчейна {blockchain}"}), 500

# Функция для проверки концентрации токенов
def check_token_concentration(contract_address, total_supply, threshold=70):
    """Проверяем концентрацию токенов на нескольких кошельках."""
    blockchain_api = BlockchainAPI("ethereum")  # Пример с Ethereum
    holder_info = blockchain_api.send_request("eth_getTokenHolders", [contract_address])

    if holder_info:
        high_concentration = [
            holder for holder in holder_info if holder['percentage'] > threshold
        ]

        if high_concentration:
            # Генерация сообщения для Telegram
            message = f"Token {contract_address} has high concentration:\n"
            for holder in high_concentration:
                message += f"Address: {holder['address']}, Balance: {holder['balance']}, Percentage: {holder['percentage']}%\n"
            send_telegram_message(message)

# Запуск Flask приложения
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
