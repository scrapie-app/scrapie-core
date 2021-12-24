from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schema import user as UserSchema
from database import models
import hashlib, uuid
from ..util import api_key_util
from time import time
from datetime import datetime


class UserRoute:
    def __init__(self, app, options) -> None:
      # Get user for user id
      @app.get("/user/{user_id}", response_model=UserSchema.User)
      def getUser(user_id: int, db: Session = Depends(options['get_db'])):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        db_user_api_quota = db.query(models.APIQuota).filter(models.APIQuota.user_id == user_id).first()
        if db_user is None:
          raise HTTPException(status_code=404, detail="User not found")
        return UserSchema.User(
          id=db_user.id,
          email=db_user.email,
          api_key=db_user_api_quota.api_key,
          quota=db_user_api_quota.quota,
          created_at=db_user.created_at,
          updated_at=db_user.updated_at
        )

      # Create a new user with email and password
      @app.post("/user", response_model=UserSchema.User)
      def createUser(user: UserSchema.UserCreate, db: Session = Depends(options['get_db'])):
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user is not None:
          raise HTTPException(status_code=400, detail="User already exists")
        salt = uuid.uuid4().hex
        encoded_string = (user.password + salt).encode('utf-8')
        hashed_password = hashlib.sha512(encoded_string).hexdigest()
        time_now = datetime.fromtimestamp(time())
        db_user = models.User(email=user.email, hashed_password=hashed_password, created_at=time_now, updated_at=time_now)
        db.add(db_user)
        db.commit()
        db.flush()
        # get the user id and create a quota for the user
        # generate the API key here
        api_key = api_key_util.generate_api_key(24)
        db_user_api_quota = models.APIQuota(user_id=db_user.id, api_key=api_key, quota=100, created_at=time_now, updated_at=time_now)
        db.add(db_user_api_quota)
        db.commit()
        return UserSchema.User(
          id=db_user.id,
          email=db_user.email,
          api_key=db_user_api_quota.api_key,
          quota=db_user_api_quota.quota,
          created_at=db_user.created_at,
          updated_at=db_user.updated_at
        )
