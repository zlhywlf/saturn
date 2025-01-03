from saturn.configs import project_config
from fakeredis import FakeRedis as Redis

redis_sync = Redis.from_url(project_config.cache_url)
