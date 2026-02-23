from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Traffic
from backend.app.schemas.traffic import TrafficCreate

router = APIRouter(prefix="/traffic", tags=["Traffic"])


@router.post("/")
def add_traffic(traffic: TrafficCreate, db: Session = Depends(get_db)):
    new_traffic = Traffic(
        route_id=traffic.route_id,
        start_time=traffic.start_time,
        end_time=traffic.end_time,
        congestion_level=traffic.congestion_level,
        traffic_reason=traffic.traffic_reason
    )

    db.add(new_traffic)
    db.commit()
    db.refresh(new_traffic)

    return {"message": "Traffic data added", "traffic_id": new_traffic.traffic_id}


@router.get("/")
def get_all_traffic(db: Session = Depends(get_db)):
    data = db.query(Traffic).all()

    result = []
    for t in data:
        item = t.__dict__
        item.pop("_sa_instance_state", None)
        result.append(item)

    return result