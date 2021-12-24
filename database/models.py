from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .connect import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  created_at = Column(DateTime, index=True)
  updated_at = Column(DateTime, index=True)

class APIQuota(Base):
  __tablename__ = 'api_quota'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), index=True)
  api_key = Column(String, unique=True, index=True)
  quota = Column(Integer)
  created_at = Column(DateTime, index=True)
  updated_at = Column(DateTime, index=True)
