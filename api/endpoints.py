class BlockchainEndpoints:
    """Класс для управления эндпоинтами блокчейнов."""

    def __init__(self):
        self.endpoints = {
            "Arbitrum": "https://arbitrum-one.public.blastapi.io",
            "Arbitrum Nova": "https://arbitrum-nova.public.blastapi.io",
            "Avalanche": "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc",
            "Ethereum": "https://eth-mainnet.public.blastapi.io",
            "Base": "https://base-mainnet.public.blastapi.io",
            "Blast": "https://blastl2-mainnet.public.blastapi.io",
            "BOB": "https://bob-mainnet.public.blastapi.io",
            "Fantom": "https://fantom-mainnet.public.blastapi.io",
            "Linea": "https://linea-mainnet.public.blastapi.io",
            "Mantle": "https://mantle-mainnet.public.blastapi.io",
            "Mode": "https://mode-mainnet.public.blastapi.io",
            "opBNB": "https://opbnb-mainnet.public.blastapi.io",
            "Optimism": "https://optimism-mainnet.public.blastapi.io",
            "Polygon": "https://polygon-mainnet.public.blastapi.io",
            "Polygon zkEVM": "https://polygon-zkevm-mainnet.public.blastapi.io",
            "Scroll": "https://scroll-mainnet.public.blastapi.io",
            "zkSync": "https://zksync-mainnet.public.blastapi.io",
        }

    def list_supported_blockchains(self):
        """
        Возвращает список поддерживаемых блокчейнов.
        """
        return list(self.endpoints.keys())

    def get_endpoint(self, blockchain):
        """
        Возвращает URL эндпоинта для указанного блокчейна.

        :param blockchain: Название блокчейна.
        :return: URL эндпоинта.
        """
        return self.endpoints.get(blockchain, None)

    def get_holders(self, platform, contract):
        """
        Возвращает фиктивные данные о держателях токена.
        """
        return [
            {"address": f"0xHolder{n}", "percent": 10 * n, "amount": 1000 * n}
            for n in range(1, 6)
        ]

    def get_token_supply(self, platform, contract):
        """
        Возвращает фиктивные данные об остатке токенов.
        """
        return {"remaining": 100000, "percent": 80}

    def get_avg_purchase_price(self, platform, contract, holders):
        """
        Возвращает фиктивную среднюю цену покупки.
        """
        return 10.5
