from fastapi import FastAPI
from .routes import api_key, scrape, users, auth, projects
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
        user_router = users.users_route_factory(options=appOptions)
        scrape_router = scrape.scrape_route_factory(options=appOptions)
        auth_router = auth.auth_route_factory(options=appOptions)
        api_key_router = api_key.api_key_route_factory(options=appOptions)
        projects_router = projects.projects_route_factory(options=appOptions)

        self.app.include_router(user_router)
        self.app.include_router(scrape_router)
        self.app.include_router(auth_router)
        self.app.include_router(api_key_router, prefix='/api')
        self.app.include_router(projects_router, prefix='/project')
        
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