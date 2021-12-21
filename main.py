import uvicorn
import logging
from fastapi import FastAPI

from models.website import Website


from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

config = Config(env_file='.env')
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

app = FastAPI()

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

log.addHandler(ch)

app.add_middleware(SessionMiddleware, secret_key="keyboard-cat")

uktier2 = Website(name="UK Tier 2", url="https://www.uk-tier2.com/", body="UK Tier 2 is a UK-based provider of IT services and solutions.", protocol="https")

@app.get("/")
def root():
  return uktier2

@app.route('/login')
async def login(request):
    redirect_url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_url)

@app.route('/auth')
async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.get_user(token)
    return user
  
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")