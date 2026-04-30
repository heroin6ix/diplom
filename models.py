from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(Text)

    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)

    phone = Column(String, unique=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")
