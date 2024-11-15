from api.telegram_bot import send_telegram_message

def notify_about_token(name, contract, blockchain, holders, message_type):
    """
    Отправляет уведомление в Telegram.
    
    :param name: Название токена
    :param contract: Адрес контракта
    :param blockchain: Блокчейн токена
    :param holders: Информация о холдерах
    :param message_type: Тип сообщения (1, 2 или 3)
    """
    message = f"{message_type}: {name} ({blockchain})\nКонтракт: {contract}\n"
    for holder in holders:
        message += f"- {holder['address']}: {holder['percentage']:.2f}%\n"
    send_telegram_message(message)
