from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class AuthRequest(BaseModel):
    code: str
    redirect_uri: str
    state: Optional[str] = None
    is_student: Optional[bool] = False
    is_instructor: Optional[bool] = False

    class Config:
        from_attributes = True
        schema_extra = {
            "examples": [
                {
                    "name": "google_student",
                    "summary": "Google OAuth student registration",
                    "value": {
                        "code": "4/0AfJohXnLWq9iBZLOz...",
                        "redirect_uri": "http://localhost:3000/api/auth/callback/google",
                        "state": "eyJzdGF0ZUlkIjoiMTIzNCIsInJlZGlyZWN0UGF0aCI6Ii9zdHVkZW50LWRhc2hib2FyZCIsInRpbWVzdGFtcCI6MTcwNzkwODgwMH0=",
                        "is_student": True,
                        "is_instructor": False
                    }
                },
                {
                    "name": "github_instructor",
                    "summary": "GitHub OAuth instructor registration",
                    "value": {
                        "code": "e72e16c7e42f292c6912...",
                        "redirect_uri": "http://localhost:3000/api/auth/callback/github",
                        "state": "eyJzdGF0ZUlkIjoiNTY3OCIsInJlZGlyZWN0UGF0aCI6Ii9tZW50b3ItZGFzaGJvYXJkIiwidGltZXN0YW1wIjoxNzA3OTA4ODAwfQ==",
                        "is_student": False,
                        "is_instructor": True
                    }
                },
                {
                    "name": "facebook_student",
                    "summary": "Facebook OAuth student registration", 
                    "value": {
                        "code": "AQBPjs3h7BXr_Qb9...",
                        "redirect_uri": "http://localhost:3000/api/auth/callback/facebook",
                        "state": "eyJzdGF0ZUlkIjoiOTAxMiIsInJlZGlyZWN0UGF0aCI6Ii9zdHVkZW50LWRhc2hib2FyZCIsInRpbWVzdGFtcCI6MTcwNzkwODgwMH0=",
                        "is_student": True,
                        "is_instructor": False
                    }
                }
            ]
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
        schema_extra = {
            "examples": [
                {
                    "name": "google_login",
                    "summary": "Example Google OAuth response",
                    "value": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user_id": 123,
                        "display_name": "John Doe",
                        "email": "john.doe@gmail.com",
                        "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                        "expires_in": 86400,
                        "redirect_path": "/student-dashboard",
                        "is_student": True,
                        "is_instructor": False
                    }
                },
                {
                    "name": "github_login",
                    "summary": "Example GitHub OAuth response",
                    "value": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user_id": 456,
                        "display_name": "Jane Smith",
                        "email": "jane.smith@github.com",
                        "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                        "expires_in": 86400,
                        "redirect_path": "/mentor-dashboard",
                        "is_student": False,
                        "is_instructor": True
                    }
                },
                {
                    "name": "facebook_login",
                    "summary": "Example Facebook OAuth response",
                    "value": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user_id": 789,
                        "display_name": "Alice Johnson",
                        "email": "alice.johnson@facebook.com",
                        "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                        "expires_in": 86400,
                        "redirect_path": "/student-dashboard",
                        "is_student": True,
                        "is_instructor": False
                    }
                }
            ]
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
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "google_student",
                    "summary": "Google OAuth student registration",
                    "value": {
                        "code": "4/0AfJohXnLWq9iBZLOz...",
                        "redirect_uri": "http://localhost:3000/api/auth/callback/google",
                        "state": "eyJzdGF0ZUlkIjoiMTIzNCIsInJlZGlyZWN0UGF0aCI6Ii9zdHVkZW50LWRhc2hib2FyZCIsInRpbWVzdGFtcCI6MTcwNzkwODgwMH0=",
                        "is_student": True,
                        "is_instructor": False
                    }
                }
            ]
        }