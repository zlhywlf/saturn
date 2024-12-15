"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.db import redis_sync


class RedisQueuePersistentSync(QueuePersistentSync):
    """redis queue persistent."""

    @override
    def get_length(self, key: str) -> int:
        res = redis_sync.zcard(key)
        return res if isinstance(res, int) else 0

    @override
    def save(self, key: str, data: bytes, priority: int) -> None:
        redis_sync.execute_command("ZADD", key, priority, data)  # type:ignore[no-untyped-call]

    @override
    def select(self, key: str, start: int, end: int, min_: int, max_: int) -> list[bytes] | None:
        with redis_sync.pipeline() as pip:
            pip.multi()
            pip.zrevrange(key, start, end)
            pip.zremrangebyrank(key, min_, max_)
            results: list[Any] = pip.execute()[0]  # type:ignore[no-untyped-call]
        return results

    @override
    def delete(self, key: str) -> None:
        redis_sync.delete(key)
