import os
from dotenv import load_dotenv

class BlockchainEndpoints:
    """Класс для управления эндпоинтами блокчейнов с поддержкой загрузки из .env файла."""
    
    def __init__(self):
        """
        Инициализация эндпоинтов.
        Эндпоинты загружаются из .env файла, если указаны. 
        Если нет, используется словарь с жестко заданными значениями.
        """
        load_dotenv()  # Загружаем переменные из .env файла

        self.endpoints = {
            "arbitrum": os.getenv("ARBITRUM", "https://arbitrum-one.public.blastapi.io"),
            "arbitrum_nova": os.getenv("ARBITRUM_NOVA", "https://arbitrum-nova.public.blastapi.io"),
            "avalanche_rpc": os.getenv("AVALANCHE_RPC", "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc"),
            "ethereum": os.getenv("ETHEREUM", "https://eth-mainnet.public.blastapi.io"),
            "base": os.getenv("BASE", "https://base-mainnet.public.blastapi.io"),
            "blast": os.getenv("BLAST", "https://blastl2-mainnet.public.blastapi.io"),
            "bob": os.getenv("BOB", "https://bob-mainnet.public.blastapi.io"),
            "fantom": os.getenv("FANTOM", "https://fantom-mainnet.public.blastapi.io"),
            "linea": os.getenv("LINEA", "https://linea-mainnet.public.blastapi.io"),
            "mantle": os.getenv("MANTLE", "https://mantle-mainnet.public.blastapi.io"),
            "mode": os.getenv("MODE", "https://mode-mainnet.public.blastapi.io"),
            "opbnb": os.getenv("OPBNB", "https://opbnb-mainnet.public.blastapi.io"),
            "optimism": os.getenv("OPTIMISM", "https://optimism-mainnet.public.blastapi.io"),
            "polygon": os.getenv("POLYGON", "https://polygon-mainnet.public.blastapi.io"),
            "polygon_zkevm": os.getenv("POLYGON_ZKEVM", "https://polygon-zkevm-mainnet.public.blastapi.io"),
            "scroll": os.getenv("SCROLL", "https://scroll-mainnet.public.blastapi.io"),
            "zksync": os.getenv("ZKSYNC", "https://zksync-mainnet.public.blastapi.io")
        }

    def get_endpoint(self, blockchain_name):
        """
        Возвращает URL-эндпоинт для указанного блокчейна.
        
        :param blockchain_name: Название блокчейна
        :return: URL-эндпоинт или None, если блокчейн не найден
        """
        return self.endpoints.get(blockchain_name)

    def list_supported_blockchains(self):
        """
        Возвращает список поддерживаемых блокчейнов.
        
        :return: Список названий блокчейнов
        """
        return list(self.endpoints.keys())

    def validate_endpoints(self):
        """
        Проверяет, доступны ли указанные эндпоинты.
        Возвращает список блокчейнов с недоступными эндпоинтами.
        """
        unavailable = []
        for blockchain, endpoint in self.endpoints.items():
            if not self._is_endpoint_reachable(endpoint):
                unavailable.append(blockchain)
        return unavailable

    @staticmethod
    def _is_endpoint_reachable(endpoint):
        """
        Проверяет доступность эндпоинта через HTTP-запрос.
        
        :param endpoint: URL-эндпоинт
        :return: True, если эндпоинт доступен, иначе False
        """
        try:
            response = requests.get(endpoint, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
