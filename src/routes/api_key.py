from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
from time import time
from database import models
from schema import user
from ..util import helper_fns, api_secrets_util

def api_key_route_factory(options):
    router = APIRouter()
    helper_fns_factory = helper_fns.create_helper_fns_factory(options)
    get_current_active_user = helper_fns_factory['get_current_active_user']
    @router.post('/create')
    def create_token(user: user.UserCreate, current_user: user.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        api_data_for_user = db.query(models.APIQuota).filter(models.APIQuota.user_id == current_user.id).first()
        if api_data_for_user is not None:
            raise HTTPException(status_code=422, detail='Cannot create API Key')
        if api_data_for_user.api_key != user.api_key:
            raise HTTPException(status_code=401, detail='invalid API key')
        # generate the API key here
        api_key = api_secrets_util.generate_api_key(24)
        time_now = datetime.fromtimestamp(time())
        db_user_api_quota = models.APIQuota(user_id=current_user.id, api_key=api_key, quota=100, created_at=time_now, updated_at=time_now)
        db.add(db_user_api_quota)
        db.commit()

    @router.post('/revoke')
    def revoke_token():
        pass
    
    @router.post('/enable')
    def enable_token():
        pass

    @router.post('/disable')
    def disable_token():
        pass

    return router
