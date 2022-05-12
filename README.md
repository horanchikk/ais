<div align="center">

# Исходный код сайта кинотеатра

</div>

## Установка зависимостей

### Для Linux

Если Вы используете операционную систему Linux, то для установки зависимостей потребуется всего лишь иметь Advanced Packaging Tool (APT). Проверить, установлен ли пакетный менеждер можно, введя команду `apt update`. Затем можно будет выполнить команду в терминале

С использованием root:

```sh
echo "Installing dependencies..." && sudo apt install python3 nodejs-lts && sudo npm --global install yarn && pip3 install uvicorn fastapi && cd frontend && yarn && cd .. && echo "Depedencies has been installed/updated!"
```

Без использования root (зачастую этот вариант требуется для Termux):

```sh
echo "Installing dependencies..." && apt install python3 nodejs-lts && npm --global install yarn && pip3 install uvicorn fastapi && cd frontend && yarn && cd .. && echo "Depedencies has been installed/updated!"
```

### Для Windows

Для установки зависимостей, Вам потребуется установить такие утилиты, как:

- NodeJS (https://nodejs.org/en/download/)
- Python 3.8 or later (https://www.python.org/downloads/)

Затем, необходимо будет установить дополнтельные пакеты в Windows Powershell:

```ps
(npm --global install yarn) -and (pip3 install uvicorn fastapi)
```

Если всё установилось без ошибок, то в терминал выведется `True`.

## Запуск сервера

### Запуск backend сервера

Для запуска backend сервера, потребуется перейти в папку "backend" и выполнить следующую команду:

```sh
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Он будет доступен по адресу: http://localhost:8000

### Запуск frontend сервера

Для запуска frontend сервера, потребуется перейти в папку "frontend" и выполнить следующую команду:

```sh
yarn dev
```

Он будет доступен по адресу: http://localhost:3000
