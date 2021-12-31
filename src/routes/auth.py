from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from schema import user as UserSchema
from database import models
import json
from ..util import api_secrets_util

def auth_route_factory(options):
    router = APIRouter()
    @router.post('/login', response_model=UserSchema.UserBearer)
    def login(user: UserSchema.UserAPILogin, db: Session = Depends(options['get_db'])):
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user is None:
            raise HTTPException(status_code=400, detail='user not found')
        # if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password):
        #     raise HTTPException(status_code=401, detail="Invalid Password")
        db_user_api_data = db.query(models.APIQuota).filter(models.APIQuota.user_id == db_user.id).first()
        if db_user_api_data is None:
            raise HTTPException(status_code=401, detail='not api quota for user')
        if db_user_api_data.api_key != user.api_key:
            raise HTTPException(status_code=401, detail='invalid API key')
        # if a bearer token doesn't exist then create it
        redis_client = options['redis']
        redis_key = f'user-session-{db_user.id}'
        redis_session_data = redis_client.get(redis_key)
        if not redis_session_data:
            user_bearer_token = api_secrets_util.generate_bearer_token(16)
            redis_login_data = json.dumps({ 'user_id': db_user.id, 'api_key': db_user_api_data.api_key, 'bearer_token': user_bearer_token })
            redis_client.set(redis_key, redis_login_data)
            redis_client.expire(redis_key, 24 * 60 * 60)

            redis_bearer_key = f'user-bearer-{user_bearer_token}'
            redis_client.set(redis_bearer_key, redis_login_data)
            redis_client.expire(redis_key, 24 * 60 * 60)
            return UserSchema.UserBearer(bearer_token=user_bearer_token)
        redis_session_data_parsed = json.loads(redis_session_data)
        return UserSchema.UserBearer(bearer_token=redis_session_data_parsed.bearer_token)
        # create a bearer token and put it in redis, expires 24 hrs
    return router
