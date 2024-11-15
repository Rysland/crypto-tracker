import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Все эндпоинты
ENDPOINTS = {
    "aptos": os.getenv("APTOS_ENDPOINT"),
    "arbitrum": os.getenv("ARBITRUM_ENDPOINT"),
    "arbitrum_nova": os.getenv("ARBITRUM_NOVA_ENDPOINT"),
    "avalanche_rpc": os.getenv("AVALANCHE_RPC_ENDPOINT"),
    "avalanche_avax": os.getenv("AVALANCHE_AVAX_ENDPOINT"),
    "avalanche_x": os.getenv("AVALANCHE_X_ENDPOINT"),
    "avalanche_p": os.getenv("AVALANCHE_P_ENDPOINT"),
    "ethereum": os.getenv("ETHEREUM_ENDPOINT"),
    "base": os.getenv("BASE_ENDPOINT"),
    "bitcoin": os.getenv("BITCOIN_ENDPOINT"),
    "blast": os.getenv("BLAST_ENDPOINT"),
    "bob": os.getenv("BOB_ENDPOINT"),
    "fantom": os.getenv("FANTOM_ENDPOINT"),
    "linea": os.getenv("LINEA_ENDPOINT"),
    "mantle": os.getenv("MANTLE_ENDPOINT"),
    "mode": os.getenv("MODE_ENDPOINT"),
    "opbnb": os.getenv("OPBNB_ENDPOINT"),
    "optimism": os.getenv("OPTIMISM_ENDPOINT"),
    "polygon": os.getenv("POLYGON_ENDPOINT"),
    "polygon_zkevm": os.getenv("POLYGON_ZKEVM_ENDPOINT"),
    "scroll": os.getenv("SCROLL_ENDPOINT"),
    "sui": os.getenv("SUI_ENDPOINT"),
    "zksync": os.getenv("ZKSYNC_ENDPOINT"),
}

def get_endpoint(blockchain_name):
    """Получает эндпоинт для указанного блокчейна."""
    return ENDPOINTS.get(blockchain_name)
