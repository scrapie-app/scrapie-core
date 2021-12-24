from sqlalchemy.orm import Session

from . import models
import schema

def get_user(db: Session, user_id: int) -> schema.user.User:
    return db.query(models.User).filter(models.User.id == user_id).first()
