from dotenv import load_dotenv
load_dotenv()
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

#Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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