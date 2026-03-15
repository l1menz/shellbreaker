from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import user, challenges, progress, nfc

#Creates DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Taskerbait API",
    description="Backend for the Taskerbait social challenge app",
    version="0.1.0",
)

# CORS: use CORS_ORIGINS env (comma-separated) or default to localhost
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
cors_origins = [o.strip() for o in _cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user.router)
app.include_router(challenges.router)
app.include_router(progress.router)
app.include_router(nfc.router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Taskerbait API is running"}