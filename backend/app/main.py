from fastapi import FastAPI
from datetime import datetime, timezone


app = FastAPI(
    title="TaskFlow API",
    description="Backend API for TaskFlow",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "application": "TaskFlow",
        "message": "Welcome to TaskFlow API",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }
