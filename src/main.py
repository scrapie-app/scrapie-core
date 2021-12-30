from .app import App
import logging
from logging.config import fileConfig
import dotenv, redis, os

dotenv.load_dotenv(f".env.{os.environ.get('NODE_ENV')}")
redisConnectionPool = redis.ConnectionPool(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'))

# fileConfig('logging_config.ini')
options = {
    'appLogger': logging.getLogger(),
    'redis': redis.Redis(connection_pool=redisConnectionPool)
}
scrapieApi = App(options)
