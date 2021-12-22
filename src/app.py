from fastapi import FastAPI
from .routes import scrape
import toml
import os

class App:
    def __new__(self, options) -> FastAPI:
        self.app = FastAPI()
        scrape.ScrapeRoute(app=self.app, options=options)

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