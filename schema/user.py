from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
  email: str

class UserCreate(UserBase):
  password: str

class User(UserBase):
  id: int
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    orm_mode = True