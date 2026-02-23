from fastapi import FastAPI
from backend.app.routers import routes, traffic, incidents, analysis
from backend.app.database import engine
from backend.app.models import Base

app = FastAPI(title="AI Traffic & Transport Intelligence System")


app.include_router(routes.router, prefix="/routes", tags=["Routes"])
app.include_router(traffic.router, prefix="/traffic", tags=["Traffic"])
app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"message": "API is running 🚦"}