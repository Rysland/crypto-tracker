import sys
import os
from api.blockchain_api import BlockchainAPI  # Убедитесь, что этот импорт работает

# Устанавливаем путь для поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

# Список поддерживаемых блокчейнов
blockchains = [
    "aptos", "arbitrum", "arbitrum_nova", "avalanche_rpc", "ethereum",
    "base", "bitcoin", "blast", "bob", "fantom", "linea", "mantle",
    "mode", "opbnb", "optimism", "polygon", "polygon_zkevm", "scroll",
    "sui", "zksync"
]

def test_endpoints():
    """Функция для тестирования эндпоинтов."""
    for blockchain in blockchains:
        print(f"Тестируем блокчейн: {blockchain}")
        try:
            # Инициализация API
            api = BlockchainAPI(blockchain)
            # Тестируем метод получения текущего блока
            result = api.send_request("eth_blockNumber", [])
            if result and 'result' in result:
                print(f"{blockchain}: Эндпоинт доступен. Текущий блок: {int(result['result'], 16)}")
            else:
                print(f"{blockchain}: Проблема с эндпоинтом. Ответ: {result}")
        except Exception as e:
            print(f"{blockchain}: Ошибка при тестировании. {e}")

# Запускаем тестирование
if __name__ == "__main__":
    test_endpoints()
