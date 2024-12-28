from typing import override

from saturn.core.rfp.RfpPersistentSync import RfpPersistentSync
from saturn.db import redis_sync


class RedisRfpPersistentSync(RfpPersistentSync):
    """redis request fingerprint persistent."""

    @override
    def save(self, key: str, data: str) -> int:
        res = redis_sync.sadd(key, data)
        return res if isinstance(res, int) else 0

    @override
    def delete(self, key: str) -> None:
        redis_sync.delete(key)

    @override
    def exist(self, key: str, data: str) -> bool:
        return self.save(key, data) == 0
