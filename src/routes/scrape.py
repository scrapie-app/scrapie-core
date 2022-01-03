import requests
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from database import models
from schema import website, user
from ..util import helper_fns

def scrape_route_factory(options):
    router = APIRouter()
    helper_fns_factory = helper_fns.create_helper_fns_factory(options)
    get_current_active_user = helper_fns_factory['get_current_active_user']
    @router.get('/scrape/ping')
    def ping(website: website.Website, current_user: user.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        options['appLogger'].debug(f'Testing website connection for {website}')
        # get session data from redis using bearer
        api_data_for_user = db.query(models.APIQuota).filter(models.APIQuota.user_id == current_user.id).first()
        if api_data_for_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API Key')
        if api_data_for_user.quota < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='API Quota Exceeded')
        api_data_for_user.quota -= 1
        db.commit()
        try:
            r = requests.get(website.url, timeout=10)
            website.url = r.url
            website.protocol = r.url[:r.url.find(':')]
            if r.status_code == status.HTTP_200_OK:
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
    return router