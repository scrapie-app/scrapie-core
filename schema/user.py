from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .apiQuota import APIQuota

class UserBase(BaseModel):
  email: str

class UserCreate(UserBase):
  hashed_password: str

class User(UserBase):
  id: int
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    orm_mode = True