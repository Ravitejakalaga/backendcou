from pydantic import BaseModel
from typing import Optional,List

class StudentRequest(BaseModel):
    user_id: int
    
class userContext(BaseModel):
    user_id: int
    challenges: Optional[List[str]] = None
   