# Telegram Bot

---

## Настройка и запуск:

1. Создайте конфиг, использовав шаблон: `cp config.example.toml config.toml`.
2. Заполните обязательные поля в файле `config.toml`:
    1. `[telegram_bot.token]` - токен бота.
    2. `[app.main_chat_id]` - ID группового чата куда будут приходить отчеты о
       завершении смены.
    3. `[app.api_base_url]` - IP или домен, на котором работает API server.
    4. `[web_app.base_url]` - URL, на котором доступно веб-приложение.
    5. `[redis.url]` - URL для подключения к Redis (например,
       `redis://localhost:6379/0`).
3. Создайте конфиг логгирования:
   `cp logging_config.example.json logging_config.json`.
4. Создайте и установите виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Запустите бота:
   ```bash
   python src/main.py
   ```
