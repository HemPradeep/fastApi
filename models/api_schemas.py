from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    user: str
    gender: str 

class CreateUser(BaseModel):
    user: str
    gender: str

class UpdateUserName(BaseModel):
    user: str