from fastapi import FastAPI
from sqlalchemy.sql.functions import mode
from .routes import scrape, users
import toml
import os

from database import models
from database.connect import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()

class App:
    def __new__(self, options) -> FastAPI:
        appProjectData = toml.load(os.path.join('pyproject.toml'))
        appPoetryData = appProjectData['tool']['poetry']
        self.app = FastAPI(
            title=appPoetryData['name'],
            version=appPoetryData['version'],
            description=appPoetryData['description']
        )
        appOptions = {
          'get_db': get_db,
          **options
        }
        scrape.ScrapeRoute(app=self.app, options=appOptions)
        users.UserRoute(app=self.app, options=appOptions)
        # home route
        @self.app.get('/')
        def home():
            appMetadata = {
                'name': appPoetryData['name'],
                'version': appPoetryData['version'],
                'author': appPoetryData['authors']
            }
            return appMetadata
        return self.app