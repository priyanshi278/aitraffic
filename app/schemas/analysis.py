from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    start_location: str
    end_location: str
