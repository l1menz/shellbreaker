from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import users, challenges, progress

#Creates DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShellBreaker API",
    description="Backend for the ShellBreaker social challenge app",
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
app.include_router(users.router)
app.include_router(challenges.router)  
app.include_router(progress.router)
app.include_router(nfc.router)
app.include_router(friends.router)
app.include_router(bets.router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "ShellBreaker API is running"}