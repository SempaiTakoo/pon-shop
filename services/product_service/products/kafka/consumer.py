from kafka import KafkaConsumer
import json
import django
import os
import sys
print("До вообще всего")
# Инициализация Django
sys.path.append('/products')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_service.settings')
django.setup()

from products.models import Product
from products.kafka.producer import send_product_price

consumer = KafkaConsumer(
    'order_service_logs',
    bootstrap_servers='kafka:9092',
    group_id='product_service_group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

print("Kafka consumer ждёт сообщений...", flush=True)

for message in consumer:
    print(f"Получено сообщение: {message.value}", flush=True)
    data = message.value["data"]
    product_id = data["product_id"]
    quantity = data["quantity"]
    order_id = data["order_id"]
    try:
        product = Product.objects.get(product_id=product_id)
        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()

            print(f"Обновлено количество товара {product_id}, теперь: {product.quantity}", flush=True)
            send_product_price({
                "order_id": order_id,
                "product_id": product.product_id,
                "price": float(product.price)
            })         # 👈 отправка обратно
        else:
            print(f"Недостаточно товара {product_id}, доступно: {product.quantity}", flush=True)

    except Product.DoesNotExist:
        print(f"❌ Продукт с id={product_id} не найден.", flush=True)
    except Exception as e:
        print(f"⚠️ Ошибка обработки сообщения: {e}", flush=True)
