import uvicorn
from src import app
import logging
from logging.config import fileConfig
import dotenv, redis, os

dotenv.load_dotenv()
redisConnectionPool = redis.ConnectionPool(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'))

# fileConfig('logging_config.ini')
options = {
    'appLogger': logging.getLogger(),
    'redis': redis.Redis(connection_pool=redisConnectionPool)
}
scrapieApi = app.App(options)

if __name__ == "__main__":
    uvicorn.run(scrapieApi, host="0.0.0.0", port=8000, log_level="info")
