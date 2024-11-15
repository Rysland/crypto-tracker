import json
import logging

CACHE_FILE = "tokens_cache.json"

def load_tokens_from_cache():
    """
    Загружает токены из кэша.
    :return: Список токенов.
    """
    try:
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Файл кэша не найден. Выполните 'update_tokens'.")
        return []
    except json.JSONDecodeError:
        logging.error("Ошибка чтения файла кэша. Выполните 'update_tokens'.")
        return []

def save_tokens_to_cache(tokens):
    """
    Сохраняет токены в кэш.
    :param tokens: Список токенов.
    """
    try:
        with open(CACHE_FILE, "w") as file:
            json.dump(tokens, file, indent=4)
        logging.info(f"Сохранено токенов в кэш: {len(tokens)}")
    except Exception as e:
        logging.error(f"Ошибка сохранения токенов в кэш: {e}")
