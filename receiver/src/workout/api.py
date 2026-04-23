from ninja import Router
from .models import TestItem

test_router = Router()

@test_router.get("/items")
def get_items(request):
    items = TestItem.objects.all().values("id", "name", "created_at")
    return list(items)

@test_router.post("/items")
def create_item(request, name: str):
    item = TestItem.objects.create(name=name)
    return {"id": item.id, "name": item.name}