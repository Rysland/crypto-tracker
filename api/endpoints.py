class BlockchainEndpoints:
    """Класс для управления эндпоинтами блокчейнов."""

    def list_supported_blockchains(self):
        """
        Возвращает список поддерживаемых блокчейнов.
        """
        return [
            "Aptos",
            "Arbitrum",
            "Arbitrum Nova",
            "Avalanche",
            "Ethereum",
            "Base",
            "Bitcoin",
            "Blast",
            "BOB",
            "Fantom",
            "Linea",
            "Mantle",
            "Mode",
            "opBNB",
            "Optimism",
            "Polygon",
            "Polygon zkEVM",
            "Scroll",
            "Sui",
            "zkSync",
        ]

    def get_endpoint(self, blockchain):
        """
        Возвращает URL эндпоинта для указанного блокчейна.

        :param blockchain: Название блокчейна.
        :return: URL эндпоинта.
        """
        endpoints = {
            "Aptos": "https://aptos-mainnet.public.blastapi.io",
            "Arbitrum": "https://arbitrum-one.public.blastapi.io",
            "Arbitrum Nova": "https://arbitrum-nova.public.blastapi.io",
            "Avalanche": "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc",
            "Ethereum": "https://eth-mainnet.public.blastapi.io",
            "Base": "https://base-mainnet.public.blastapi.io",
            "Bitcoin": "https://bitcoin-mainnet.public.blastapi.io",
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
            "Sui": "https://sui-mainnet.public.blastapi.io",
            "zkSync": "https://zksync-mainnet.public.blastapi.io",
        }

        return endpoints.get(blockchain, None)
