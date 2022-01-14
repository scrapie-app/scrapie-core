from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class APIQuotaBase(BaseModel):
  id: int
  user_id: int
  api_key: str
  quota: int
  active: bool
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

class APIKey(BaseModel):
  api_key: str

class APIQuota(APIQuotaBase):
  class Config:
    orm_mode = True
