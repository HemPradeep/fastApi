from fastapi import FastAPI
from models.user_inmemory import UserManager
from models.UserResponse import UserResponse

app = FastAPI()
manager = UserManager()

@app.get("/api/users", response_model=list[UserResponse])
def getUsers():
    return manager.getUsers()
