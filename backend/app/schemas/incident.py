from pydantic import BaseModel

class IncidentCreate(BaseModel):
    route_id: int
    reason: str
    severity: str
    reported_at: str
