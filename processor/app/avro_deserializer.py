import io
import struct

import httpx
import fastavro
from functools import lru_cache


class AvroDeserializer:
    def __init__(self, schema_registry_url: str):
        self.url = schema_registry_url.rstrip("/")
        self._cache: dict[int, dict] = {}

    async def _get_schema(self, schema_id: int) -> dict:
        if schema_id in self._cache:
            return self._cache[schema_id]
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.url}/schemas/ids/{schema_id}")
            r.raise_for_status()
        import json
        schema = fastavro.parse_schema(json.loads(r.json()["schema"]))
        self._cache[schema_id] = schema
        return schema

    async def deserialize(self, raw_bytes: bytes) -> dict:
        schema_id = struct.unpack(">I", raw_bytes[1:5])[0]
        schema = await self._get_schema(schema_id)
        return fastavro.schemaless_reader(io.BytesIO(raw_bytes[5:]), schema)
