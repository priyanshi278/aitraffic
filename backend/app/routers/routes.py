from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Route
from backend.app.schemas.route import RouteCreate

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.post("/")
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    new_route = Route(
        start_location=route.start_location,
        end_location=route.end_location,
        via_locations=route.via_locations,
        distance_km=route.distance_km,
        average_time_min=route.average_time_min
    )

    db.add(new_route)
    db.commit()
    db.refresh(new_route)

    return {"message": "Route created successfully", "route_id": new_route.route_id}


@router.get("/")
def get_all_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()

    result = []
    for r in routes:
        data = r.__dict__
        data.pop("_sa_instance_state", None)
        result.append(data)

    return result