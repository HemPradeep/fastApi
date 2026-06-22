from fastapi import FastAPI
from models.user_inmemory import UserManager
from models.api_schemas import UserResponse, CreateUser

app = FastAPI()
manager = UserManager()

@app.get("/api/users", response_model=list[UserResponse])
def getUsers():
    return manager.getUsers()

@app.post("/api/users", response_model=UserResponse)
def addAUser(userData: CreateUser):
    return manager.addUser(userData.user, userData.gender)