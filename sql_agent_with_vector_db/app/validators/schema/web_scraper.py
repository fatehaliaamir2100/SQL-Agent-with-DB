from pydantic import BaseModel

class ScraperData(BaseModel):
    url: str
    query: str
    department: str
    customer_id: int
    updated: bool
