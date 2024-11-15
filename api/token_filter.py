import logging

def filter_tokens_by_contract(tokens):
    """
    Фильтрует токены, оставляя только те, у которых есть адреса контрактов.
    :param tokens: Список токенов.
    :return: Список токенов с адресами контрактов.
    """
    try:
        filtered_tokens = []
        for token in tokens:
            if token.get("contract"):
                filtered_tokens.append(token)
            else:
                logging.warning(f"Токен {token['name']} ({token['symbol']}) не имеет привязки к платформе.")
        return filtered_tokens
    except Exception as e:
        logging.error(f"Ошибка фильтрации токенов: {e}")
        return []
