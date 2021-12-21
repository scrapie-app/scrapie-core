from pydantic import BaseModel

class Website(BaseModel):
  name: str
  url: str
  body: str
  protocol: str