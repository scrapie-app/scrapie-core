from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    pass

class Project(ProjectBase):
    class Config:
        orm_mode = True
