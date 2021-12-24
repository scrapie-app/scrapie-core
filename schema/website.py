from typing import Optional
from pydantic import BaseModel

class Website(BaseModel):
  name: str
  url: str
  body: Optional[str] = None
  protocol: Optional[str] = None
  dnsResolved: bool = False
  reachable: bool = False
