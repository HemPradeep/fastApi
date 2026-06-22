from fastapi import FastAPI, status
from models.user_inmemory import UserManager
from models.api_schemas import UserResponse, CreateUser, UpdateUserName

app = FastAPI()
manager = UserManager()

@app.get("/api/users", response_model=list[UserResponse],status_code=status.HTTP_200_OK)
def getUsers():
    return manager.getUsers()

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def addAUser(userData: CreateUser):
    return manager.addUser(userData.user, userData.gender)

@app.put("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def updateUser(id: int, request: UpdateUserName):
    return manager.editUserData(id, request.user)

@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    manager.deleteAUser(id)