from ninja import Router

from django.conf import settings
from django.http import JsonResponse

from workout.models import TestItem
from core.kafka_producer import KafkaProducer


test_router = Router()

@test_router.get("/items")
def get_items(request):
    items = TestItem.objects.all().values("id", "name", "created_at")
    return list(items)

@test_router.post("/items")
def create_item(request, name: str):
    item = TestItem.objects.create(name=name)
    return {"id": item.id, "name": item.name}



# producer = KafkaProducer({
#     "KAFKA_BOOTSTRAP_SERVERS": settings.KAFKA_BOOTSTRAP_SERVERS,
#     "KAFKA_TOPIC": settings.KAFKA_TOPIC,
#     "SCHEMA_REGISTRY_URL": settings.SCHEMA_REGISTRY_URL,
#     "AVRO_SCHEMA_PATH": settings.AVRO_SCHEMA_PATH, 
# })
producer = KafkaProducer({
    "KAFKA_BOOTSTRAP_SERVERS": "kafka:9092",
    "KAFKA_TOPIC": "tracker.events",
    "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
    "AVRO_SCHEMA_PATH": "/app/schemas/workout_event.avsc",
})

@test_router.post("/kafka")
def test_kafka(request):
    producer.send(
        key="test-key",
        value={"user_id": 1, "event": "workout", "type": "run", "distance": 10.0}
    )
    producer.flush()
    return JsonResponse({"status": "sent"})