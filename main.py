from fastapi import FastAPI
from models.user_inmemory import UserManager
from models.api_schemas import UserResponse, CreateUser, UpdateUserName

app = FastAPI()
manager = UserManager()

@app.get("/api/users", response_model=list[UserResponse])
def getUsers():
    return manager.getUsers()

@app.post("/api/users", response_model=UserResponse)
def addAUser(userData: CreateUser):
    return manager.addUser(userData.user, userData.gender)

@app.put("/api/users/{id}", response_model=UserResponse)
def update_user(id: int, request: UpdateUserName):
    return manager.editUserData(id, request.user)