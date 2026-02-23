from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Route, Traffic, Incident
from backend.app.services.route_analysis_service import analyze_routes
from backend.app.services.ai_service import rule_based_summary, groq_summary

router = APIRouter(prefix="/analysis", tags=["AI Analysis"])


@router.get("/route")
def analyze_route(start_location: str, end_location: str, db: Session = Depends(get_db)):

    routes = db.query(Route).filter(
        Route.start_location == start_location,
        Route.end_location == end_location
    ).all()

    traffics = db.query(Traffic).all()
    incidents = db.query(Incident).all()

    # ORM → dict
    routes_data = [r.__dict__ for r in routes]
    traffics_data = [t.__dict__ for t in traffics]
    incidents_data = [i.__dict__ for i in incidents]

    # remove SQLAlchemy internal key
    for item in routes_data + traffics_data + incidents_data:
        item.pop("_sa_instance_state", None)

    # Route Scoring
    routes_analysis = analyze_routes(routes_data, traffics_data, incidents_data)

    # Rule-Based Decision
    rule_result = rule_based_summary(routes_analysis)

    # AI Decision
    ai_result = groq_summary(routes_analysis)

    return {
        "routes_analysis": routes_analysis,
        "rule_based_decision": rule_result,
        "ai_decision": ai_result
    }