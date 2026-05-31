from fastapi import FastAPI

from app.api.routers.auth import router as auth_router

from app.api.routers.jobs import router as jobs_router

app = FastAPI(title="Job Tracker API")

app.include_router(auth_router)
app.include_router(jobs_router)

@app.get("/health")
def health():
    return {"status": "ok"}

