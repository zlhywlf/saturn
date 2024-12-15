from redis import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from saturn.configs import project_config

redis_sync = Redis.from_url(project_config.cache_url)
db_async = engine = create_async_engine(project_config.db_url, echo=project_config.debug)
