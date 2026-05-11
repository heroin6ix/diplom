from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

class RequestStatusResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ServiceResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    class Config:
        from_attributes = True

class RequestCreate(BaseModel):
    description: str
    device_type: str | None = None
    device_model: str | None = None
    serial_number: str | None = None

class RequestUpdate(BaseModel):
    description: str | None = None
    diagnostic_result: str | None = None
    estimated_price: Decimal | None = None
    final_price: Decimal | None = None
    status_id: int | None = None

class RequestResponse(BaseModel):
    id: int 
    description: str 
    device_type: str | None
    device_model: str | None
    serial_number: str | None
    diagnostic_result: str | None 
    estimated_price: Decimal | None
    final_price: Decimal | None
    created_at: datetime
    completed_at: datetime | None
    updated_at: datetime | None
    
    status: RequestStatusResponse
    services: list[ServiceResponse]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
