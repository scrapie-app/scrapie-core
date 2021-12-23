from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schema import user
from database import models

class UserRoute:
    def __init__(self, app, options) -> None:
        @app.get("/user/{user_id}", response_model=user.User)
        def getUser(user_id: int, db: Session = Depends(options['get_db'])):
          db_user =db.query(models.User).filter(models.User.id == user_id).first()
          if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
          return db_user
            