from pydantic import BaseModel
from typing import List

class Requirement(BaseModel):
    id: str
    statement: str
    priority: str
    constraints: List[str]
    speaker: str
    confidence: float
