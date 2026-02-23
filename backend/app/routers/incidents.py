from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Incident
from backend.app.schemas.incident import IncidentCreate

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/")
def add_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    new_incident = Incident(
        route_id=incident.route_id,
        reason=incident.reason,
        severity=incident.severity,
        reported_at=incident.reported_at
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return {"message": "Incident reported", "incident_id": new_incident.incident_id}


@router.get("/")
def get_all_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()

    # ORM → dict
    result = []
    for i in incidents:
        data = i.__dict__
        data.pop("_sa_instance_state", None)
        result.append(data)

    return result