#!/bin/sh

until pg_isready -h user_service_db -p 5432; do
  echo "Waiting for Postgres..."
  sleep 5
done

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn main:app --host 0.0.0.0 --port 8001
