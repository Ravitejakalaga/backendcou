from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class AuthRequest(BaseModel):
    code: str
    redirect_uri: str
    state: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "code": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "redirect_uri": "http://localhost:3000/callback",
                "state": "eyJzdGF0ZUlkIjoiMTIzNCIsInJlZGlyZWN0UGF0aCI6Ii9kYXNoYm9hcmQiLCJ0aW1lc3RhbXAiOjE3MDc5MDg4MDB9"
            }
        }

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    display_name: str
    email: Optional[str] = None
    profile_image: Optional[str] = None
    expires_in: int = Field(default=86400)  # 1 day in seconds
    redirect_path: Optional[str] = None
    is_student: Optional[bool] = False
    is_instructor: Optional[bool] = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": 123,
                "display_name": "John Doe",
                "email": "john.doe@example.com",
                "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                "expires_in": 86400,
                "redirect_path": "/dashboard",
                "is_student": True,
                "is_instructor": False
            }
        }

class StateData(BaseModel):
    stateId: str
    redirectPath: str
    timestamp: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "stateId": "1234",
                "redirectPath": "/dashboard",
                "timestamp": 1707908800  # Example timestamp
            }
        }

class EmailAuthRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecureP@ssw0rd123"
            }
        }

class EmailRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_student: Optional[bool] = False
    is_instructor: Optional[bool] = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecureP@ssw0rd123",
                "first_name": "John",
                "last_name": "Doe",
                "is_student": True,
                "is_instructor": False
            }
        }

class GoogleAuthRequest(AuthRequest):
    """Google OAuth authentication request schema"""
    pass  # Uses the same fields as base AuthRequest