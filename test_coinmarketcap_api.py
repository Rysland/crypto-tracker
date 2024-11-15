from api.coinmarketcap_api import CoinMarketCapAPI

def test_get_top_tokens():
    """Тестируем функцию получения топ-токенов."""
    cmc = CoinMarketCapAPI()
    tokens = cmc.get_top_tokens(limit=10)
    
    if tokens:
        print("Полученные токены:")
        for token in tokens:
            print(f"{token['name']} ({token['symbol']})")
    else:
        print("Не удалось получить список токенов.")

if __name__ == "__main__":
    test_get_top_tokens()
