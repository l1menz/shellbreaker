from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/nfc", tags=["nfc"])

VALID_TAG_TYPES = {"fitness", "social", "career", "skills"}
CHALLENGES_PER_TAG = 10


def _categories_to_str(categories: list) -> str:
    return ",".join([c.value if hasattr(c, "value") else c for c in categories])


@router.post("/register", response_model=schemas.NFCTagOut, status_code=201)
def register_tag(
    body: schemas.NFCTagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Register an NFC tag for the current user.
    Each user can only have one tag — call PATCH /nfc/me to update it.
    """
    if current_user.nfc_tag:
        raise HTTPException(status_code=400, detail="You already have an NFC tag registered. Use PATCH /nfc/me to update it.")

    tag = models.NFCTag(
        owner_id=current_user.id,
        enabled_categories=_categories_to_str(body.enabled_categories),
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/me", response_model=schemas.NFCTagOut)
def get_my_tag(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get the current user's NFC tag profile."""
    if not current_user.nfc_tag:
        raise HTTPException(status_code=404, detail="No NFC tag registered. POST /nfc/register first.")
    return current_user.nfc_tag


@router.patch("/me", response_model=schemas.NFCTagOut)
def update_tag(
    body: schemas.NFCTagUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Update the enabled challenge categories on your NFC tag."""
    tag = current_user.nfc_tag
    if not tag:
        raise HTTPException(status_code=404, detail="No NFC tag registered.")

    if body.enabled_categories is not None:
        tag.enabled_categories = _categories_to_str(body.enabled_categories)

    db.commit()
    db.refresh(tag)
    return tag


@router.post("/checkin", response_model=schemas.NFCTagOut)
def checkin(
    body: schemas.NFCCheckin,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Called when a user scans an NFC tag (their own or someone else's).
    - Updates last_checkin timestamp on the tag owner's profile.
    - Refreshes health_score back to 100.
    - Returns the scanned tag's profile so the scanner can see
      what categories the tag owner plays and potentially challenge them.
    """
    tag_owner = db.query(models.User).filter(models.User.id == body.tag_owner_id).first()
    if not tag_owner or not tag_owner.nfc_tag:
        raise HTTPException(status_code=404, detail="NFC tag not found for that user.")

    tag = tag_owner.nfc_tag
    tag.last_checkin = datetime.now(timezone.utc)
    tag.health_score = 100

    db.commit()
    db.refresh(tag)
    return tag


@router.post("/scan", response_model=list[schemas.UserChallengeOut])
def scan_tag(
    body: schemas.NFCTagScan,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Called when a user scans an NFC tag (e.g. at a gym, cafe).
    The tag has a type (fitness, social, career, skills) and ~10 built-in challenges.
    Assigns those challenges to the user, replacing any current incomplete tasks.
    """
    tag_type = body.tag_type.lower().strip()
    if tag_type not in VALID_TAG_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tag_type. Must be one of: {', '.join(VALID_TAG_TYPES)}",
        )

    # Get challenges for this tag type
    challenges = (
        db.query(models.Challenge)
        .filter(models.Challenge.tag_type == tag_type, models.Challenge.is_active == True)
        .limit(CHALLENGES_PER_TAG)
        .all()
    )
    if not challenges:
        raise HTTPException(status_code=404, detail=f"No challenges found for tag type '{tag_type}'")

    # Remove user's current incomplete tasks (so we replace with tag's challenges)
    db.query(models.UserChallengeProgress).filter(
        models.UserChallengeProgress.user_id == current_user.id,
        models.UserChallengeProgress.status != models.ChallengeStatus.completed,
    ).delete()

    # Assign the tag's challenges to the user
    assignments = []
    for challenge in challenges:
        uc = models.UserChallengeProgress(user_id=current_user.id, challenge_id=challenge.id)
        db.add(uc)
        assignments.append(uc)

    db.commit()
    for uc in assignments:
        db.refresh(uc)

    return assignments


@router.get("/{user_id}", response_model=schemas.NFCTagOut)
def get_tag_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Public endpoint — look up any user's NFC tag profile by user ID.
    Used after scanning a tag to display their challenge categories.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.nfc_tag:
        raise HTTPException(status_code=404, detail="NFC tag not found.")
    return user.nfc_tag