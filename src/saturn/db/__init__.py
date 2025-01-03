from fakeredis import FakeRedis
from redis import Redis

from saturn.configs import project_config

redis_sync = Redis.from_url(project_config.cache_url) if project_config.cache_url else FakeRedis()
