from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class ProjectBase(BaseModel):
  id: int
  user_id: int
  name: str
  description: str
  api_key_id: int
  active: bool
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

class ProjectData(BaseModel):
  name: str
  description: str
  api_key_id: int

class ProjectID(BaseModel):
  id: int

class ProjectsData(BaseModel):
  projects: List[ProjectBase]

class Project(ProjectBase):
    class Config:
        orm_mode = True
