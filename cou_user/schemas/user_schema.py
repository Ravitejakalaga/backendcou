from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from base64 import b64encode

class UserBase(SQLModel):
    display_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    work_email: Optional[str] = None
    personal_email: Optional[str] = None
    role_id: Optional[int] = None
    login_type_id: Optional[int] = None
    mobile: Optional[str] = None
    affiliate_id: Optional[int] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    youtube: Optional[str] = None
    monitor: Optional[bool] = False
    remarks: Optional[str] = None
    currency_id: Optional[int] = None
    country_id: Optional[int] = None
    is_student: Optional[bool] = False
    is_instructor: Optional[bool] = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "display_name": "John Doe",
                "first_name": "John",
                "last_name": "Doe",
                "work_email": "john.doe@company.com",
                "personal_email": "john.doe@example.com",
                "role_id": 2,
                "login_type_id": 6,
                "mobile": "+1234567890",
                "affiliate_id": 1,
                "facebook": "https://facebook.com/johndoe",
                "instagram": "https://instagram.com/johndoe",
                "linkedin": "https://linkedin.com/in/johndoe",
                "twitter": "https://twitter.com/johndoe",
                "youtube": "https://youtube.com/c/johndoe",
                "monitor": False,
                "remarks": "Some notes about the user",
                "currency_id": 1,
                "country_id": 1,
                "is_student": True,
                "is_instructor": False
            }
        }

class UserCreate(UserBase):
    created_by: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "display_name": "John Doe",
                "first_name": "John",
                "last_name": "Doe",
                "personal_email": "john.doe@example.com",
                "role_id": 2,
                "login_type_id": 6,
                "is_student": True,
                "is_instructor": False,
                "created_by": 1
            }
        }

class UserUpdate(SQLModel):
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    work_email: Optional[str] = None
    personal_email: Optional[str] = None
    role_id: Optional[int] = None
    login_type_id: Optional[int] = None
    mobile: Optional[str] = None
    active: Optional[bool] = None
    premium: Optional[bool] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    youtube: Optional[str] = None
    monitor: Optional[bool] = None
    remarks: Optional[str] = None
    currency_id: Optional[int] = None
    country_id: Optional[int] = None
    is_student: Optional[bool] = None
    is_instructor: Optional[bool] = None
    updated_by: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "display_name": "John Doe Updated",
                "first_name": "John",
                "last_name": "Doe",
                "personal_email": "john.doe.updated@example.com",
                "mobile": "+1234567890",
                "active": True,
                "premium": True,
                "is_student": True,
                "is_instructor": True,
                "updated_by": 1
            }
        }

class UserRead(UserBase):
    id: int
    image_base64: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    active: bool
    premium: bool
    created_by: int
    updated_by: int

    @staticmethod
    def from_orm(user):
        # Create a dict of the user data
        data = {
            field: getattr(user, field)
            for field in UserRead.__fields__.keys()
            if field != 'image_base64'
        }
        
        # Convert mobile number to string if it exists
        if data.get('mobile') is not None:
            data['mobile'] = str(data['mobile'])
        
        # Convert bytes image to base64 if it exists
        if user.image:
            try:
                data['image_base64'] = b64encode(user.image).decode('utf-8')
            except Exception:
                data['image_base64'] = None
        else:
            data['image_base64'] = None
            
        return UserRead(**data)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 123,
                "display_name": "John Doe",
                "first_name": "John",
                "last_name": "Doe",
                "work_email": "john.doe@company.com",
                "personal_email": "john.doe@example.com",
                "role_id": 2,
                "login_type_id": 6,
                "mobile": "+1234567890",
                "affiliate_id": 1,
                "facebook": "https://facebook.com/johndoe",
                "instagram": "https://instagram.com/johndoe",
                "linkedin": "https://linkedin.com/in/johndoe",
                "twitter": "https://twitter.com/johndoe",
                "youtube": "https://youtube.com/c/johndoe",
                "monitor": False,
                "remarks": "Some notes about the user",
                "currency_id": 1,
                "country_id": 1,
                "is_student": True,
                "is_instructor": False,
                "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                "created_at": "2024-02-14T12:00:00Z",
                "updated_at": "2024-02-14T12:00:00Z",
                "active": True,
                "premium": False,
                "created_by": 1,
                "updated_by": 1
            }
        }