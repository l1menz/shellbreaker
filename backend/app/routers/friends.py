from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/friends", tags=["friends"])


def _get_accepted_friend_ids(db: Session, user_id: int) -> list[int]:
    """Helper: return list of user IDs who are confirmed friends with user_id."""
    friendships = (
        db.query(models.Friendship)
        .filter(
            models.Friendship.status == models.FriendStatus.accepted,
            or_(
                models.Friendship.requester_id == user_id,
                models.Friendship.addressee_id == user_id,
            ),
        )
        .all()
    )
    return [
        f.addressee_id if f.requester_id == user_id else f.requester_id
        for f in friendships
    ]


@router.post("/request", response_model=schemas.FriendRequestOut, status_code=201)
def send_request(
    body: schemas.FriendRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Send a friend request by username."""
    target = db.query(models.User).filter(models.User.username == body.addressee_username).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found.")
    if target.id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't friend yourself.")

    # Check if a relationship already exists in either direction
    existing = (
        db.query(models.Friendship)
        .filter(
            or_(
                and_(
                    models.Friendship.requester_id == current_user.id,
                    models.Friendship.addressee_id == target.id,
                ),
                and_(
                    models.Friendship.requester_id == target.id,
                    models.Friendship.addressee_id == current_user.id,
                ),
            )
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Friend relationship already exists (status: {existing.status}).")

    friendship = models.Friendship(requester_id=current_user.id, addressee_id=target.id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


@router.get("/requests/incoming", response_model=list[schemas.FriendRequestOut])
def incoming_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get all pending friend requests sent TO the current user."""
    return (
        db.query(models.Friendship)
        .filter(
            models.Friendship.addressee_id == current_user.id,
            models.Friendship.status == models.FriendStatus.pending,
        )
        .all()
    )


@router.post("/requests/respond", response_model=schemas.FriendRequestOut)
def respond_to_request(
    body: schemas.FriendRequestAction,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Accept or decline an incoming friend request."""
    if body.action not in ("accept", "decline"):
        raise HTTPException(status_code=400, detail="action must be 'accept' or 'decline'.")

    friendship = (
        db.query(models.Friendship)
        .filter(
            models.Friendship.id == body.friendship_id,
            models.Friendship.addressee_id == current_user.id,
            models.Friendship.status == models.FriendStatus.pending,
        )
        .first()
    )
    if not friendship:
        raise HTTPException(status_code=404, detail="Pending friend request not found.")

    friendship.status = (
        models.FriendStatus.accepted if body.action == "accept" else models.FriendStatus.declined
    )
    db.commit()
    db.refresh(friendship)
    return friendship


@router.get("/", response_model=list[schemas.UserPublic])
def list_friends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """List all accepted friends for the current user."""
    friend_ids = _get_accepted_friend_ids(db, current_user.id)
    if not friend_ids:
        return []
    return db.query(models.User).filter(models.User.id.in_(friend_ids)).all()


@router.get("/leaderboard", response_model=list[schemas.UserPublic])
def friends_leaderboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """XP leaderboard scoped to the current user's friend network (includes self)."""
    friend_ids = _get_accepted_friend_ids(db, current_user.id)
    ids_to_rank = friend_ids + [current_user.id]
    return (
        db.query(models.User)
        .filter(models.User.id.in_(ids_to_rank))
        .order_by(models.User.xp.desc())
        .all()
    )