from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.app.database import Base

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(Integer, primary_key=True, index=True)
    start_location = Column(String)
    end_location = Column(String)
    via_locations = Column(String)
    distance_km = Column(Float)
    average_time_min = Column(Float)


class Traffic(Base):
    __tablename__ = "traffic"

    traffic_id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.route_id"))
    start_time = Column(String)
    end_time = Column(String)
    congestion_level = Column(String)
    traffic_reason = Column(String)


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.route_id"))
    reason = Column(String)
    severity = Column(String)
    reported_at = Column(String)