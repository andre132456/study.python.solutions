from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    """DTO for creating a new user."""

    name: str
    email: EmailStr


class UserResponse(BaseModel):
    """DTO for user response."""

    id: str
    name: str
    email: str

    class Config:
        from_attributes = True
