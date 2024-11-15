import requests
from api.endpoints import get_endpoint

class BlockchainAPI:
    def __init__(self, blockchain_name):
        self.endpoint = get_endpoint(blockchain_name)
        if not self.endpoint:
            raise ValueError(f"Эндпоинт для блокчейна '{blockchain_name}' не найден.")

    def send_request(self, method, params=[]):
        """Отправляет JSON-RPC запрос к указанному эндпоинту."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

