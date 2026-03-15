from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timezone
import random

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/progress", tags=["progress"])

DAILY_CHALLENGE_COUNT = 3


@router.get("/today", response_model=list[schemas.UserChallengeOut])
def get_todays_challenges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Return the current user's active challenges.
    - If they have incomplete tasks (from NFC scan or previous assignment), return those.
    - If none, randomly assign DAILY_CHALLENGE_COUNT challenges as fallback.
    """
    existing = (
        db.query(models.UserChallengeProgress)
        .filter(
            models.UserChallengeProgress.user_id == current_user.id,
            models.UserChallengeProgress.status != models.ChallengeStatus.completed,
        )
        .order_by(models.UserChallengeProgress.assigned_at.desc())
        .all()
    )

    if existing:
        return existing

    # Fallback: assign random challenges (user hasn't scanned NFC yet)
    all_challenges = db.query(models.Challenge).filter(models.Challenge.is_active == True).all()
    selected = random.sample(all_challenges, min(DAILY_CHALLENGE_COUNT, len(all_challenges)))

    assignments = []
    for challenge in selected:
        uc = models.UserChallengeProgress(user_id=current_user.id, challenge_id=challenge.id)
        db.add(uc)
        assignments.append(uc)

    db.commit()
    for uc in assignments:
        db.refresh(uc)

    return assignments


@router.post("/complete", response_model=schemas.UserChallengeOut)
def complete_challenge(
    body: schemas.CompleteChallenge,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Mark a UserChallenge as completed and award XP to the user."""
    uc = (
        db.query(models.UserChallengeProgress)
        .filter(
            models.UserChallengeProgress.id == body.user_challenge_id,
            models.UserChallengeProgress.user_id == current_user.id,
        )
        .first()
    )

    if not uc:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if uc.status == models.ChallengeStatus.completed:
        raise HTTPException(status_code=400, detail="Challenge already completed")

    uc.status = models.ChallengeStatus.completed
    uc.completed_at = datetime.now(timezone.utc)

    # Award XP and coins
    current_user.xp += uc.challenge.xp_reward
    current_user.coins += getattr(uc.challenge, "coin_reward", 0) or 0

    db.commit()
    db.refresh(uc)
    return uc


@router.get("/history", response_model=list[schemas.UserChallengeOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Return all challenge attempts for the current user."""
    return (
        db.query(models.UserChallengeProgress)
        .filter(models.UserChallengeProgress.user_id == current_user.id)
        .order_by(models.UserChallengeProgress.assigned_at.desc())
        .all()
    )