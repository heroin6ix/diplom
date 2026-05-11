from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    TIMESTAMP,
    Numeric,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

request_services = Table(
    "request_services",
    Base.metadata,
    Column("request_id", Integer, ForeignKey("requests.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))

    phone = Column(String(20), unique=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)
    requests = relationship("Request", back_populates="user")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    specialization = Column(String(100))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="employee")
    assignments = relationship("RequestAssignment", back_populates="employee")


class RequestStatus(Base):
    __tablename__ = "request_statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    requests = relationship("Request", back_populates="status")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    requests = relationship(
        "Request", secondary=request_services, back_populates="services"
    )


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    device_type = Column(String(100))
    device_model = Column(String(150))
    serial_number = Column(String(150))
    diagnostic_result = Column(Text)
    estimated_price = Column(Numeric(10, 2))
    final_price = Column(Numeric(10, 2))
    status_id = Column(Integer, ForeignKey("request_statuses.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="requests")
    status = relationship("RequestStatus", back_populates="requests")
    services = relationship(
        "Service", secondary=request_services, back_populates="requests"
    )
    assignments = relationship("RequestAssignment", back_populates="request")


class RequestAssignment(Base):
    __tablename__ = "request_assignments"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    assigned_at = Column(TIMESTAMP, default=datetime.utcnow)

    request = relationship("Request", back_populates="assignments")

    employee = relationship("Employee", back_populates="assignments")
