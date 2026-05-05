from pydantic import BaseModel

class Gap(BaseModel):
    gap_id: str
    type: str
    description: str
    requirement_ref: str
    solution_ref: str
    suggested_action: str
    confidence: float
