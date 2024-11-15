from api.coinmarketcap_api import CoinMarketCapAPI
from api.endpoints import BlockchainEndpoints
from api.blockchain_api import BlockchainAPI
import logging

def filter_tokens_by_contract(tokens):
    """
    Фильтрует токены, проверяя адрес контракта на всех поддерживаемых блокчейнах.

    :param tokens: Список токенов из CoinMarketCap.
    :return: Список токенов, найденных в поддерживаемых блокчейнах.
    """
    logging.info("Начало фильтрации токенов по адресам контрактов...")
    filtered_tokens = []

    # Список поддерживаемых блокчейнов
    endpoints = BlockchainEndpoints()
    supported_blockchains = endpoints.list_supported_blockchains()

    for token in tokens:
        contract_found = False
        for blockchain in supported_blockchains:
            try:
                blockchain_api = BlockchainAPI(blockchain)
                # Проверяем, есть ли информация по контракту на этом блокчейне
                if blockchain_api.check_contract(token["contract"]):
                    filtered_tokens.append({
                        "name": token["name"],
                        "symbol": token["symbol"],
                        "contract": token["contract"],
                        "blockchain": blockchain
                    })
                    contract_found = True
                    break  # Если нашли блокчейн, переходим к следующему токену
            except Exception as e:
                logging.error(f"Ошибка проверки контракта {token['contract']} в блокчейне {blockchain}: {e}")
        
        if not contract_found:
            logging.warning(f"Токен {token['name']} ({token['contract']}) не найден в поддерживаемых блокчейнах.")

    if not filtered_tokens:
        logging.error("Фильтрация токенов не дала результатов. Проверьте список поддерживаемых блокчейнов.")
    else:
        logging.info(f"Успешно отфильтровано токенов: {len(filtered_tokens)}")
    return filtered_tokens
