from pydantic import BaseModel
from typing import List

class Solution(BaseModel):
    id: str
    decision: str
    tech: List[str]
    limitations: List[str]
    type: str
    confidence: float
