import logging
from logging import Logger
from fastapi import FastAPI
from .routes import scrape
import toml
import os

def appLogging(appName, logLevel = logging.DEBUG) -> Logger:
    log = logging.getLogger(appName)
    log.setLevel(logLevel)
    ch = logging.StreamHandler()
    ch.setLevel(logLevel)
    log.addHandler(ch)
    return log

class App:
    def __new__(self) -> FastAPI:
        self.app = FastAPI()
        self.appLogger = appLogging("scrapie-app", logging.DEBUG)
        options = {
            'appLogger': self.appLogger,
        }
        scrape.ScrapeRoute(self.app, options)

        # home route
        @self.app.get('/')
        def home():
            appProjectData = toml.load(os.path.join('pyproject.toml'))
            appPoetryData = appProjectData['tool']['poetry']
            appMetadata = {
                'name': appPoetryData['name'],
                'version': appPoetryData['version'],
                'author': appPoetryData['authors']
            }
            return appMetadata
        return self.app