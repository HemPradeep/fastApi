from fastapi import FastAPI, status, HTTPException
from models.user_inmemory import UserManager
from models.api_schemas import UserResponse, CreateUser, UpdateUserName

app = FastAPI()
manager = UserManager()

@app.get("/api/users", response_model=list[UserResponse],status_code=status.HTTP_200_OK)
def get_all_users():
        return manager.getUsers()

@app.get("/api/users/{id}", response_model=UserResponse,status_code=status.HTTP_200_OK)
def get_user_by_id(id:int):
        if not manager.doesUserExists(id):
              raise HTTPException(status_code=404, detail=f"invalid userId: {id}")
        return manager.getUserById(id)

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_a_user(userData: CreateUser):
    if (not userData.user.isalpha()) or  userData.gender not in ["M", "F", "Other"]:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User data {userData}")
    return manager.addUser(userData.user, userData.gender)

@app.put("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, request: UpdateUserName):
    if (not manager.doesUserExists(id)) or (not request.user.isalpha()):
              raise HTTPException(status_code=404, detail=f"invalid Credentials: {id}, {request.user}")
    return manager.editUserData(id, request.user)

@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    if not manager.doesUserExists(id):
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    manager.deleteAUser(id)