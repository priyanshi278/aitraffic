from pydantic import BaseModel

class TrafficCreate(BaseModel):
    route_id: int
    start_time: str
    end_time: str
    congestion_level: str
    traffic_reason: str
