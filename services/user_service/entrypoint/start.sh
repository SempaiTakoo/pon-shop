#!/bin/sh

# База данных уже должна быть готова благодаря healthcheck в docker-compose
echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
