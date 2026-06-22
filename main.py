from fastapi import FastAPI, status, HTTPException
from models.api_schemas import UserResponse, CreateUser, UpdateUserName
from models.user_db import UserDataManager
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

manager = UserDataManager()

@app.get("/api/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    return manager.get_all_users()

@app.get("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int):
    user = manager.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    return user

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_a_user(userData: CreateUser):
    if not userData.user.isalpha() or userData.gender not in ["Male", "Female", "Other"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data")
    return manager.add_a_user(userData.user, userData.gender)

@app.put("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, request: UpdateUserName):
    if not request.user.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user name")
    if not manager.does_user_exist(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    return manager.update_user_name(id, request.user)

@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    if not manager.does_user_exist(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    manager.delete_user(id)
