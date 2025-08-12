from pydantic import BaseModel

class StudentRequest(BaseModel):
    user_id: int
