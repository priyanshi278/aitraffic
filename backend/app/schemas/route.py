from pydantic import BaseModel

class RouteCreate(BaseModel):
    start_location: str
    end_location: str
    via_locations: str
    distance_km: float
    average_time_min: float
