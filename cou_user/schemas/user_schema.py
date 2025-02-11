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

class UserCreate(UserBase):
    created_by: int

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
        orm_mode = True