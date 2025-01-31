import datetime
import json
import pickle
from typing import Any

import ujson

from app.core.helpers.cache.base import BaseBackend
from app.core.helpers.redis import redis_client


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)


class RedisBackend(BaseBackend):
    async def get(self, *, key: str) -> Any:
        result = await redis_client.get(key)
        if not result:
            return

        try:
            data = pickle.loads(result)
        except:
            data = ujson.loads(result)

        return data

    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(
                response,
            )
        else:
            response = pickle.dumps(response)

        await redis_client.set(name=key, value=response, ex=ttl)

    async def delete_startswith(self, *, value: str) -> None:
        async for key in redis_client.scan_iter(f"{value}*"):
            await redis_client.delete(key)
