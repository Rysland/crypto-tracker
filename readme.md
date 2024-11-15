Crypto Tracker
Crypto Tracker — это приложение для отслеживания данных блокчейнов, анализа распределения токенов и уведомлений в Telegram.

Установка
Клонируйте репозиторий:
git clone https://github.com/Rysland/crypto-tracker.git
cd crypto-tracker
Установите зависимости:

bash Копировать код pip install -r requirements.txt Настройте файл .env:

Создайте файл .env в корневой папке и добавьте в него: plaintext Копировать код TELEGRAM_TOKEN=your_telegram_token TELEGRAM_CHAT_ID=your_chat_id FLASK_SECRET_KEY=your_flask_secret_key

Blockchain endpoints
APTOS_ENDPOINT=https://aptos-mainnet.public.blastapi.io ... Запуск Запустите Flask-приложение:

bash Копировать код python3 web/app.py Откройте браузер и перейдите:

Главная страница: http://localhost:5000 Тестирование эндпоинтов: http://localhost:5000/test/ Тестирование Запустите скрипт для тестирования всех эндпоинтов: bash Копировать код python3 test_endpoints.py Функциональность Мониторинг блокчейнов: Отслеживание блоков, транзакций и токенов через Blast API. Анализ концентрации токенов: Автоматическое выявление токенов с высоким распределением среди нескольких кошельков. Уведомления Telegram: Уведомления о концентрации токенов и других событиях. Поддерживаемые блокчейны Список поддерживаемых блокчейнов:

Aptos Arbitrum Avalanche Ethereum Polygon zkSync И другие...
