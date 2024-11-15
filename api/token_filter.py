from api.coinmarketcap_api import CoinMarketCapAPI
from api.endpoints import BlockchainEndpoints

def filter_tokens_by_blockchain(limit=1000):
    """
    Фильтрует токены по поддерживаемым блокчейнам и возвращает их контракты.
    
    :param limit: Количество токенов для обработки (по умолчанию 1000).
    :return: Список токенов с их контрактами и блокчейнами.
    """
    try:
        # Инициализация API
        cmc = CoinMarketCapAPI()
        endpoints = BlockchainEndpoints()
        
        # Получаем список поддерживаемых блокчейнов
        supported_blockchains = endpoints.list_supported_blockchains()
        
        # Получаем список топ-токенов
        tokens = cmc.get_top_tokens(limit=limit)
        if not tokens:
            raise ValueError("Не удалось получить список токенов с CoinMarketCap.")
        
        filtered_tokens = []

        # Фильтруем токены по поддерживаемым блокчейнам
        for token in tokens:
            platforms = token.get("platforms", {})
            for blockchain, contract_address in platforms.items():
                if blockchain in supported_blockchains:
                    filtered_tokens.append({
                        "name": token["name"],
                        "symbol": token["symbol"],
                        "contract": contract_address,
                        "blockchain": blockchain
                    })
        
        return filtered_tokens

    except Exception as e:
        print(f"Ошибка в процессе фильтрации токенов: {e}")
        return []
