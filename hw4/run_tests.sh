#!/bin/bash

# Имя сервиса в вашем docker-compose.yml, который содержит ваш Django проект
SERVICE_NAME=web

# Если аргумент передан, используем его для тестов
TEST_PATH=${1:-}

# Преобразуем путь в точечное имя модуля, если он указан как путь к файлу
if [[ $TEST_PATH == *.py ]]; then
  TEST_PATH=$(echo $TEST_PATH | sed 's|/|.|g' | sed 's|.py$||')
fi

# Запуск тестов внутри контейнера
docker-compose exec $SERVICE_NAME bash -c "python manage.py test $TEST_PATH"
