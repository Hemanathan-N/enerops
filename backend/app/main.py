from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_user

app = FastAPI(title="EnerOps AI Platform", version="1.0.0", dependencies=[Depends(get_current_user)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import energy, ai, hierarchy, production, cost, reports

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(energy.router)
app.include_router(ai.router)
app.include_router(hierarchy.router)
app.include_router(production.router)
app.include_router(cost.router)
app.include_router(reports.router)

