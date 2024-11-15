import requests
from api.endpoints import get_endpoint

class BlockchainAPI:
    """Класс для взаимодействия с блокчейн-эндпоинтами."""
    
    def __init__(self, blockchain_name):
        """Инициализация с указанием имени блокчейна."""
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
            data = response.json()
            if "error" in data:
                raise ValueError(f"Ошибка в ответе API: {data['error']}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка данных: {e}")
            return None
