from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("/", response_model=list[schemas.ChallengeOut])
def list_challenges(db: Session = Depends(get_db)):
    """Return all available challenges."""
    return db.query(models.Challenge).all()


@router.get("/{challenge_id}", response_model=schemas.ChallengeOut)
def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    """Return a single challenge by ID."""
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge