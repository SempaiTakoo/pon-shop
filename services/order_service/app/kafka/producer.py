from kafka import KafkaProducer
from app.core.config import settings
import json
import os

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
KAFKA_TOPIC = settings.KAFKA_ORDER_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

def send_order_event(event: dict, key: str = "order_created"):
    try:
        producer.send(KAFKA_TOPIC, key=key, value=event)
        producer.flush()
        print(f"[Kafka] Event sent: {event}")
    except Exception as e:
        print(f"[Kafka] Error sending event: {e}")
