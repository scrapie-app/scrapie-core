from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
  email: str

class UserCreate(UserBase):
  password: str

class UserLogin(UserCreate):
  pass

class UserAPILogin(UserBase):
  api_key: str

class UserBearer(BaseModel):
  bearer_token: str

class User(UserBase):
  id: int
  api_key: Optional[str] = None
  quota: Optional[int] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    orm_mode = True