from pydantic import BaseModel
from typing import Optional

class InferenceRequest(BaseModel):
    query: str
    department: str
    customer_id: int
    updated: bool
    url: Optional[str] = None
    web_data: Optional[str] = None

class InferenceResponse(BaseModel):
    response: str
