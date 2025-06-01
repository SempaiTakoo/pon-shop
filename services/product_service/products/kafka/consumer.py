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
consumer = KafkaConsumer(
    'order_service_logs',
    bootstrap_servers='kafka:9092',
    group_id='product_service_group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

print("🟢 Kafka consumer ждёт сообщений...", flush=True)

for message in consumer:
    print(f"📦 Получено сообщение: {message.value}", flush=True)
    event = message.value
    data = event.get('data')

    product_id = data['product_id']
    qty_ordered = data['quantity']

    try:
        product = Product.objects.get(product_id=product_id)
        product.quantity = max(product.quantity - qty_ordered, 0)
        product.save()
        print(f"✅ Обновлён товар {product_id}: осталось {product.quantity}", flush=True)
    except Product.DoesNotExist:
        print(f"⚠️ Товар с ID {product_id} не найден.", flush=True)
