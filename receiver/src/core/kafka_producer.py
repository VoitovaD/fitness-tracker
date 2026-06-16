from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
import logging

logger = logging.getLogger(__name__)


# def workout_event_to_dict(obj: dict, ctx) -> dict:
#     return obj


class KafkaProducer:
    def __init__(self, config: dict):
        schema_registry_client = SchemaRegistryClient({
            "url": config["SCHEMA_REGISTRY_URL"],
        })
        with open(config["AVRO_SCHEMA_PATH"]) as f:
            schema_str = f.read()
        self.avro_serializer = AvroSerializer(
            schema_registry_client,
            schema_str,
            lambda obj, ctx: obj,
        )

        self.producer = Producer({
            "bootstrap.servers": config["KAFKA_BOOTSTRAP_SERVERS"],
            "security.protocol": config.get("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
            "sasl.mechanism": config.get("KAFKA_SASL_MECHANISM", "PLAIN"),
            "sasl.username": config.get("KAFKA_SASL_USERNAME", ""),
            "sasl.password": config.get("KAFKA_SASL_PASSWORD", ""),
        })
        self.topic = config["KAFKA_TOPIC"]

    def send(self, key: str, value: dict):
        self.producer.produce(
            topic=self.topic,
            key=key.encode("utf-8"),
            value=self.avro_serializer(
                value,
                SerializationContext(self.topic, MessageField.VALUE),
            ),
            callback=self.delivery_report,
        )
        self.producer.poll(0)

    def delivery_report(self, err, msg):
        if err:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.info(f"Delivered to {msg.topic()} [{msg.partition()}]")

    def flush(self):
        self.producer.flush()