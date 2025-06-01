FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x ./entrypoint/start.sh

ENTRYPOINT ["./entrypoint/start.sh"]
