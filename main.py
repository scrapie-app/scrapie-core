import uvicorn
from src import app
import logging
from logging.config import fileConfig

# fileConfig('logging_config.ini')
options = {
    'appLogger': logging.getLogger()
}
scrapieApi = app.App(options)

if __name__ == "__main__":
    uvicorn.run(scrapieApi, host="0.0.0.0", port=8000, log_level="info")
