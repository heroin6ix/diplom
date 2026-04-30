from pydantic import BaseModel


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
