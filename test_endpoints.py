from api.blockchain_api import BlockchainAPI

# Список поддерживаемых блокчейнов
blockchains = [
    "arbitrum",
    "arbitrum_nova",
    "avalanche_rpc",
    "ethereum",
    "base",
    "blast",
    "bob",
    "fantom",
    "linea",
    "mantle",
    "mode",
    "opbnb",
    "optimism",
    "polygon",
    "polygon_zkevm",
    "scroll",
    "zksync"
]

def test_endpoints():
    for blockchain in blockchains:
        print(f"Тестируем блокчейн: {blockchain}")
        try:
            api = BlockchainAPI(blockchain)
            result = api.send_request("eth_blockNumber", [])
            if result and 'result' in result:
                print(f"{blockchain}: Эндпоинт доступен. Текущий блок: {int(result['result'], 16)}")
            else:
                print(f"{blockchain}: Проблема с эндпоинтом. Ответ: {result}")
        except Exception as e:
            print(f"{blockchain}: Ошибка при тестировании. {e}")

# Запуск тестирования
if __name__ == "__main__":
    test_endpoints()
