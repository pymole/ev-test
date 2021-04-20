# Тестирование Edge Vision

Перед запуском инфраструктуры рекомендуется ознакомиться с документацией
компонентов системы:
- [Controller](controller/README.md)
- [Sensor](sensor/README.md)
- [Manipulator](manipulator/README.md)

# Локальный запуск инфраструктуры

Локальный запуск инфраструктуры осуществляется с помощью docker-compose.

Собрать образы:
```commandline
docker-compose build
```

Запустить контейнеры:
```commandline
docker-compose up -d --scale sensor=8
```

Значение параметра **--scale sensor=** отвечает за количество
контейнеров сервиса **sensor**.

Остановить контейнеры:
```commandline
docker-compose down
```

Запустить одной командой (сключая сборку образа и поднятие сервисов):
```commandline
docker-compose up -d --build --scale sensor=8
```

Посмотреть логи определенного контейнера:
```commandline
docker logs <container-hash>
```

# Переменные среды

В каждом сервисе для удобства тестирование находится шаблон файла **.env**.

_**ИСПОЛЬЗОВАТЬ ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!**_

### ADMIN_API_KEY

Пароль администратора (посылается в заголовке **API-Key** для получения
команд).

### MANIPULATOR_HOST

Хост манипулятора

### MANIPULATOR_PORT

Порт манипулятора

### REDIS_URL

Адрес подключения к Redis.

### DB_HOST

Хост для подключения к БД

### DB_PORT

Порт для подключения к БД

### DB_USER

Пользователь БД

### DB_PASSWORD

Пароль пользователя БД

### DB_NAME

Имя БД

### CONTROLLER_URL

Эндпоинт, на который сенсор будет отсылать метки.

### TIMEOUT

Сколько сенсор ждет перед отправкой следующей метки в секундах.
