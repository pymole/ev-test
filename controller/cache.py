from typing import Optional

from aioredis import Redis, create_redis_pool

import settings


connection: Optional[Redis] = None


async def init_cache():
    global connection
    connection = await create_redis_pool(settings.global_settings.redis_url, encoding='utf-8')
