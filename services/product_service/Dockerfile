# Используем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /products

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда по умолчанию (можно переопределить в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
