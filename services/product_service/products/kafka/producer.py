# products/kafka/producer.py
from kafka import KafkaProducer
import json

def send_product_price(event: dict, key: str = "product_price"):
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8")
        )
        producer.send("product_service_logs", key=key, value=event)
        producer.flush()
        print(f"[Kafka] Sent price event: {event}", flush=True)
    except Exception as e:
        print(f"[Kafka] Error sending product price: {e}", flush=True)
