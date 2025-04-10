from fastapi import FastAPI
from .api import product_api, analytics_api
from .dependencies import get_db
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Подключаем роутеры
app.include_router(product_api.router)
app.include_router(analytics_api.router)

# Метрики Prometheus
Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup():
    # Инициализация подключений
    await get_db.init_db()

@app.on_event("shutdown")
async def shutdown():
    # Корректное закрытие подключений
    await get_db.close_db()