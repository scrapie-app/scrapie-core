from typing import Optional
from pydantic import BaseModel

class APIQuotaBase(BaseModel):
  id: int
  user_id: int
  api_key: str
  quota: int
  active: bool
  created_at: Optional[str] = None
  updated_at: Optional[str] = None

class APIQuota(APIQuotaBase):
  class Config:
    orm_mode = True
