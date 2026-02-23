from fastapi import FastAPI
from app.routers import routes, traffic, incidents, analysis
from app.database import engine
from app.models import Base

app = FastAPI(title="AI Traffic & Transport Intelligence System")

# Create tables only once on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(routes.router, prefix="/routes", tags=["Routes"])
app.include_router(traffic.router, prefix="/traffic", tags=["Traffic"])
app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"message": "API is running 🚦"}