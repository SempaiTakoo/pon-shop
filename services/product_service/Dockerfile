FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей для psycopg2 и других библиотек
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости отдельно для кеширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]