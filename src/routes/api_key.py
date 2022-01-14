from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from time import time
from constants import messages
from database import models
from schema import user as UserSchema, apiQuota as APIQuota
from ..util import helper_fns, api_secrets_util

def api_key_route_factory(options):
    router = APIRouter()
    helper_fns_factory = helper_fns.create_helper_fns_factory(options)
    get_current_active_user = helper_fns_factory['get_current_active_user']

    @router.post('/create', response_model=UserSchema.User)
    def create_api_key(current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        api_data_for_user = db.query(models.APIQuota).filter(models.APIQuota.user_id == current_user.id).all()
        if len(api_data_for_user) >= 5:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=messages.API_KEYS_LIMIT_EXCEEDED)
        # generate the API key here
        api_key = api_secrets_util.generate_api_key(24)
        time_now = datetime.fromtimestamp(time())
        db_user_api_quota = models.APIQuota(user_id=current_user.id, api_key=api_key, quota=100, active=True, created_at=time_now, updated_at=time_now)
        db.add(db_user_api_quota)
        db.commit()
        return UserSchema.User(
          id=current_user.id,
          email=current_user.email,
          api_key=db_user_api_quota.api_key,
          quota=db_user_api_quota.quota,
          created_at=current_user.created_at,
          updated_at=current_user.updated_at
        )

    @router.post('/revoke', response_model=APIQuota.APIQuotaBase)
    def revoke_api_key(api_key: APIQuota.APIKey, current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        db_user_api_quota_data_for_api_key = db.query(models.APIQuota).filter(
            and_(
                models.APIQuota.user_id == current_user.id,
                models.APIQuota.api_key == api_key,
            )
        ).first()
        if not db_user_api_quota_data_for_api_key:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.INVALID_API_KEY)
        db_user_api_quota_data_for_api_key.active = False
        db_user_api_quota_data_for_api_key.updated_at = datetime.fromtimestamp(time())
        db.commit()
        return db_user_api_quota_data_for_api_key


    @router.get('/keys')
    def get_all_api_keys(current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        db_user_api_quota_data = db.query(models.APIQuota).filter(models.APIQuota.user_id == current_user.id).all()
        api_keys_data = []
        for api_data in db_user_api_quota_data:
            api_keys_data.append(UserSchema.UserAPIData(
                id=api_data.id,
                api_key=api_data.api_key,
                quota=api_data.quota,
                active=api_data.active,
                created_at=api_data.created_at,
                updated_at=api_data.updated_at,
            ))
        return UserSchema.UserAPIKeysResponse(
            id=current_user.id,
            api_keys=api_keys_data,
        )

    return router
