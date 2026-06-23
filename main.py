from fastapi import FastAPI, status, HTTPException, Depends
from src.models.api_schemas import UserResponse, CreateUser, UpdateUserName
from src.models.user_db import UserRepository
from dotenv import load_dotenv
from src.database_connection import get_user_repository

load_dotenv()
app = FastAPI()


@app.get("/api/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(manager: UserRepository = Depends(get_user_repository)):
    return manager.get_all_users()

@app.get("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, manager: UserRepository = Depends(get_user_repository)):
    user = manager.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    return user

@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_a_user(userData: CreateUser, manager: UserRepository = Depends(get_user_repository)):
    if not userData.user.isalpha() or userData.gender not in ["Male", "Female", "Other"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data")
    return manager.add_a_user(userData.user, userData.gender)

@app.put("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, request: UpdateUserName, manager: UserRepository = Depends(get_user_repository)):
    if not request.user.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user name")
    if not manager.does_user_exist(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    return manager.update_user_name(id, request.user)

@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, manager: UserRepository = Depends(get_user_repository)):
    if not manager.does_user_exist(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}")
    manager.delete_user(id)
