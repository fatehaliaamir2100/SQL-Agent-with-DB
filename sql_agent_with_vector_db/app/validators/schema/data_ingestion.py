from pydantic import BaseModel
from typing import Dict

class IngestionData(BaseModel):
    data: Dict[str, str]
    department: str
