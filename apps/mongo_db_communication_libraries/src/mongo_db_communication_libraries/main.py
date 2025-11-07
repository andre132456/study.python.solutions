import os
from contextlib import asynccontextmanager

from beanie import PydanticObjectId
from fastapi import FastAPI, HTTPException, status
from mongo_db_communication_libraries.repositories.beanie_repository import (
    BeanieRepository,
)
from mongo_db_communication_libraries.schemas.user_schema import (
    UserCreateRequest,
    UserResponse,
)

# Initialize repository with environment variables
repo = BeanieRepository(
    connection_string=os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
    database_name=os.getenv("DATABASE_NAME", "users_db"),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup database connection."""
    await repo.initialize()
    yield
    await repo.close()


app = FastAPI(title="User Management API", lifespan=lifespan)


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest):
    """Create a new user."""
    user = await repo.create_user(name=user_data.name, email=user_data.email)
    return UserResponse(id=str(user.id), name=user.name, email=user.email)


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a user by ID."""
    try:
        async with repo.client.start_session() as session:
            async with session.start_transaction():
                user = await repo.get_user_by_id(
                    PydanticObjectId(user_id), session=session
                )
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                    )
        return UserResponse(id=str(user.id), name=user.name, email=user.email)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete a user by ID."""
    try:
        deleted = await repo.delete_user(PydanticObjectId(user_id))
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )
