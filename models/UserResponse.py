from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    user: str
    gender: str 
