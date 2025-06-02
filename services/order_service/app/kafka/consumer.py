from kafka import KafkaConsumer
from app.db.session import SessionLocal
from app.db.models import Order as ORMOrder
import json
import time


print('До вообще всего', flush=True)

consumer = KafkaConsumer(
    'product_service_logs',
    bootstrap_servers='kafka:9092',
    group_id='order_service_group_4',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8')
)

print("OrderService Kafka consumer запущен и слушает 'product_service_logs'...", flush=True)

while True:
    print('Первая ступень', flush=True)
    try:
        print('Вторая ступень', flush=True)
        for msg in consumer:
            print(f"⬇️ Принято сообщение с ключом {msg.key} и значением {msg.value}", flush=True)
            key = msg.key
            value = msg.value

            order_id = value.get("order_id")
            price = value.get("price")
            print(f"Получена цена товара для заказа {order_id}: {price}", flush=True)
            with SessionLocal() as db:
                order = db.query(ORMOrder).filter_by(order_id=order_id).first()
                if order:
                    order.total_price = order.quantity * price
                    db.commit()
                    print(f"Обновлён order_id={order_id} с total_price={order.total_price}", flush=True)
                else:
                    print(f"Заказ с order_id={order_id} не найден", flush=True)

    except Exception as e:
        print(f"Ошибка consumer'а: {e}", flush=True)
        time.sleep(5)
