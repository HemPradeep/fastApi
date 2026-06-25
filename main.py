from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status

from src.database_connection import get_user_repository
from src.models.api_schemas import CreateUser, UpdateUserName, UserResponse
from src.models.user_db import UserRepository

load_dotenv()
app = FastAPI()


@app.get(
    "/api/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK
)
def get_all_users(
    manager: Annotated[UserRepository, Depends(get_user_repository)],
) -> list[UserResponse]:
    return manager.get_all_users()


@app.get("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(
    id: int, manager: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserResponse:
    user = manager.get_user_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}"
        )
    return user


@app.post(
    "/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def add_a_user(
    userData: CreateUser,
    manager: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserResponse:
    if not userData.user.isalpha() or userData.gender not in [
        "Male",
        "Female",
        "Other",
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data"
        )
    new_user = manager.add_a_user(userData.user, userData.gender)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )
    return new_user


@app.put("/api/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    request: UpdateUserName,
    manager: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserResponse:
    if not request.user.isalpha():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user name"
        )
    if not manager.does_user_exist(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}"
        )
    updated_user = manager.update_user_name(id, request.user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        )
    return updated_user


@app.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int, manager: Annotated[UserRepository, Depends(get_user_repository)]
) -> None:
    if not manager.does_user_exist(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid userId: {id}"
        )
    manager.delete_user(id)

