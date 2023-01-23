# Телеграм бот для цветочного магазина

Телеграм бот для продаважи цветочных букетов онлайн

## Настройка среды выполнения

Для запуска проекта необходимо создать переменные окружения, которые записываются в `.env` файл.

```python
DJANGO_SECRET_KEY=<YOUR-DJANGO-SECRET-KEY>
TELEGRAM_BOT_TOKEN=<YOUR-TELEGRAM-BOT-TOKEN>
```

Затем установить зависимости:

```phyton
pip install -r requirements.txt
```

Выполнить миграцию базы данных:

```python
python3 manage.py migrate
```

## Запуск сервиса

Бот работает через API с внутренним сервисом, который использует [Django](https://www.django-rest-framework.org/),
поэтому необходимо запустить проект django перед началом работы бота. Для этого запуксакются команды:

```python
python3 manage.py runserver

python3 19_telega.py
```
