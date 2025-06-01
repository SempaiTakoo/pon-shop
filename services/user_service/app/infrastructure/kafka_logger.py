from collections.abc import Callable
import json

from kafka import KafkaProducer, KafkaConsumer


class MessageBrokerLogger:
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


class MessageBrokerConsumer:
    def __init__(self, broker_url: str, topic: str) -> None:
        self.topic = topic

        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[broker_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='review-service-consumer',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def consume_logs(self, handle_event: Callable[[dict], None]):
        for message in self.consumer:
            event_data: dict = message.value
            handle_event(event_data)
