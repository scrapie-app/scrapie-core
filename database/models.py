from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql.expression import null
from .connect import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String(512))
  created_at = Column(DateTime, index=True)
  updated_at = Column(DateTime, index=True)

class APIQuota(Base):
  __tablename__ = 'api_quota'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), index=True)
  api_key = Column(String, unique=True, index=True)
  quota = Column(Integer)
  active = Column(Boolean, default=False)
  created_at = Column(DateTime, index=True)
  updated_at = Column(DateTime, index=True)

class Projects(Base):
  __tablename__ = 'projects'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), index=True)
  name = Column(String, nullable=False)
  description = Column(String, default='')
  api_key_id = Column(Integer, ForeignKey('api_quota.id'), index=True)
  active = Column(Boolean, default=False)
  created_at = Column(DateTime, index=True)
  updated_at = Column(DateTime, index=True)
