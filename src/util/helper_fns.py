import json
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.sql.functions import current_user
from schema import user
from database import models
from constants import messages

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_helper_fns_factory(options):
    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(options['get_db'])):
        # fetch the user here
        redis_client = options['redis']
        redis_user_for_bearer = redis_client.get(f'user-bearer-{token}')
        if not redis_user_for_bearer:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.UNAUTHORIZED_USER)
        redis_user_session_data = json.loads(redis_user_for_bearer)
        user = db.query(models.User).filter(models.User.id == redis_user_session_data['user_id']).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def get_current_active_user(current_user: user.UserResponse = Depends(get_current_user)):
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return current_user

    return {
        'get_current_active_user': get_current_active_user
    }
