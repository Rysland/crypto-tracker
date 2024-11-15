import requests
from api.endpoints import BlockchainEndpoints

class BlockchainAPI:
    """Класс для взаимодействия с блокчейн-эндпоинтами."""
    
    def __init__(self, blockchain_name):
        """
        Инициализация с указанием имени блокчейна.
        
        :param blockchain_name: Название блокчейна
        """
        endpoints = BlockchainEndpoints()  # Инициализация класса для эндпоинтов
        self.endpoint = endpoints.get_endpoint(blockchain_name)
        if not self.endpoint:
            raise ValueError(f"Эндпоинт для блокчейна '{blockchain_name}' не найден.")

    def send_request(self, method, params=[]):
        """
        Отправляет JSON-RPC запрос к указанному эндпоинту.
        
        :param method: Метод JSON-RPC (например, "eth_blockNumber")
        :param params: Параметры запроса
        :return: Ответ от API в формате словаря
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        try:
            print(f"Отправка запроса к {self.endpoint} с методом {method} и параметрами {params}")
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

            # Проверяем наличие ошибок в ответе
            if "error" in data:
                raise ValueError(f"Ошибка в ответе API: {data['error']}")
            
            print(f"Успешный ответ: {data}")
            return data

        except requests.exceptions.HTTPError as e:
            print(f"HTTP ошибка: {e.response.status_code} - {e.response.reason}")
            return None
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения с блокчейн-эндпоинтом.")
            return None
        except requests.exceptions.Timeout:
            print("Тайм-аут запроса.")
            return None
        except ValueError as e:
            print(f"Ошибка данных: {e}")
            return None
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            return None

    def get_block_number(self):
        """
        Получает текущий номер блока.
        
        :return: Номер блока в виде целого числа или None при ошибке
        """
        response = self.send_request("eth_blockNumber")
        if response and "result" in response:
            try:
                # Преобразуем номер блока из hex в десятичное число
                return int(response["result"], 16)
            except ValueError:
                print("Ошибка преобразования номера блока.")
                return None
        return None
