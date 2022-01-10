from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from schema import user as UserSchema
from database import models
import json
import bcrypt
from ..util import api_secrets_util, helper_fns

def auth_route_factory(options):
    router = APIRouter()
    helper_fns_factory = helper_fns.create_helper_fns_factory(options)
    get_current_active_user = helper_fns_factory['get_current_active_user']
    @router.post('/login', response_model=UserSchema.UserBearer)
    def login(user: UserSchema.UserLogin, db: Session = Depends(options['get_db'])):
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not found')
        if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
        redis_client = options['redis']
        redis_key = f'user-session-{db_user.id}'
        redis_session_data = redis_client.get(redis_key)
        if not redis_session_data:
            user_bearer_token = api_secrets_util.generate_bearer_token(16)
            redis_login_data = json.dumps({ 'user_id': db_user.id, 'bearer_token': user_bearer_token })
            redis_client.set(redis_key, redis_login_data)
            redis_client.expire(redis_key, 24 * 60 * 60)

            redis_bearer_key = f'user-bearer-{user_bearer_token}'
            redis_client.set(redis_bearer_key, redis_login_data)
            redis_client.expire(redis_key, 24 * 60 * 60)
            return UserSchema.UserBearer(bearer_token=user_bearer_token)
        redis_session_data_parsed = json.loads(redis_session_data)
        return UserSchema.UserBearer(bearer_token=redis_session_data_parsed['bearer_token'])

    @router.post('/logout')
    def logout(current_user: UserSchema.UserResponse = Depends(get_current_active_user)):
        print(current_user)
    return router
