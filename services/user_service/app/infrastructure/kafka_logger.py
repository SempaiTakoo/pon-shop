import json
import time

from kafka import KafkaProducer


class KafkaLogger:
    def __init__(self, broker_url: str, topic: str) -> None:
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=[broker_url],
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )

    def log(self, event: str, data: dict) -> None:
        message = {
            'event': event,
            'data': data
        }
        self.producer.send(topic=self.topic, value=message)
        self.producer.flush()
