from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
  id: int
  user_id: int
  api_key_id: int
  created_at: Optional[str] = None
  updated_at: Optional[str] = None

class Project(ProjectBase):
    class Config:
        orm_mode = True
