from pydantic import BaseModel
from typing import Any

class ResponseOK(BaseModel): 
    success: bool = True

class ResponseData(BaseModel):
    success: bool = True
    data: Any


