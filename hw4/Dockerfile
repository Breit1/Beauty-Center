# Используем официальный образ Python
FROM python:3.12

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y netcat-openbsd gcc postgresql-client libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в рабочую директорию
COPY . /app/

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Добавляем команду для запуска сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
