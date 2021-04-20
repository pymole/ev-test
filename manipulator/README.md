# Manipulator

Манипулятор прослушивает порт, принимает команды от контроллера и
выводит их в логи.

# Переменные среды

Переменные среды помещаются в **.env** файл.

### MANIPULATOR_HOST

Хост манипулятора

### MANIPULATOR_PORT

Порт манипулятора

# Запуск в Docker

Сборка образа:
```commandline
docker build . -t manipulator
```

Запуск контейнера:
```commandline
docker run -p 4001:4001 manipulator
```
