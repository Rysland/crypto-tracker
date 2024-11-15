import requests

class BlockchainAPI:
    """Класс для взаимодействия с блокчейн-сканерами."""

    def __init__(self, blockchain_name):
        self.blockchain_name = blockchain_name
        self.endpoint = self.get_endpoint(blockchain_name)

    def get_endpoint(self, blockchain_name):
        # Реализация получения эндпоинта для указанного блокчейна
        ...

    def check_contract(self, contract):
        """
        Проверяет, существует ли контракт на блокчейне.
        
        :param contract: Адрес контракта токена.
        :return: True, если контракт найден, иначе False.
        """
        try:
            # Пример запроса для проверки контракта
            response = requests.post(self.endpoint, json={
                "jsonrpc": "2.0",
                "method": "eth_getCode",
                "params": [contract, "latest"],
                "id": 1
            })
            response.raise_for_status()
            data = response.json()
            # Если контракт имеет код (не пустой), значит он существует
            return data.get("result") not in [None, "0x", "0x0"]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при проверке контракта {contract}: {e}")
            return False
