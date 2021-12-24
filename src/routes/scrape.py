import requests, json
from fastapi import Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import models
from schema import website

class ScrapeRoute:
    def __init__(self, app, options) -> None:
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
        @app.get('/scrape/ping')
        def ping(website: website.Website, token: str = Depends(oauth2_scheme), db: Session = Depends(options['get_db'])):
            options['appLogger'].debug(f'Testing website connection for {website}')
            # get session data from redis using bearer
            redis_client = options['redis']
            redis_user_for_bearer = redis_client.get(f'user-bearer-{token}')
            if not redis_user_for_bearer:
                raise HTTPException(status_code=401, detail='Unauthorized user')
            redis_user_session_data = json.loads(redis_user_for_bearer)
            api_data_for_user = db.query(models.APIQuota).filter(models.APIQuota.api_key == redis_user_session_data['api_key']).first()
            if api_data_for_user is None:
                raise HTTPException(status_code=401, detail='Invalid API Key')
            if api_data_for_user.quota < 1:
                raise HTTPException(status_code=400, detail='API Quota Exceeded')
            api_data_for_user.quota -= 1
            db.commit()
            try:
                r = requests.get(website.url, timeout=10)
                website.url = r.url
                website.protocol = r.url[:r.url.find(':')]
                if r.status_code == 200:
                    website.body = r.text
                    website.reachable = True
                    website.dnsResolved = True
            except requests.exceptions.TooManyRedirects as te:
                website.reachable = False
                website.dnsResolved = True
            except requests.ConnectionError as e:
                if 'nodename nor servname provided, or not known' in str(e):
                    website.dnsResolved = False
            except requests.exceptions.RequestException:
                pass
            return website