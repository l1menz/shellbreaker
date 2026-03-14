from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import DifficultyLevel, ChallengeStatus, ChallengeCategory, FriendStatus, BetStatus


# ── Auth ────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ── User ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    xp: int
    streak: int
    coins: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    """Minimal user info for leaderboards / friend lists."""
    id: int
    username: str
    xp: int
    streak: int
    coins: int

    class Config:
        from_attributes = True


# ── Challenge ────────────────────────────────────────────────────────────────

class ChallengeOut(BaseModel):
    id: int
    title: str
    description: str
    difficulty: DifficultyLevel
    category: ChallengeCategory
    points: int

    class Config:
        from_attributes = True


# ── UserChallenge (progress) ─────────────────────────────────────────────────

class UserChallengeOut(BaseModel):
    id: int
    challenge: ChallengeOut
    status: ChallengeStatus
    assigned_date: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompleteChallenge(BaseModel):
    """Request body when marking a challenge complete."""
    user_challenge_id: int


# ── NFC Tag ───────────────────────────────────────────────────────────────────

class NFCTagCreate(BaseModel):
    enabled_categories: List[ChallengeCategory]


class NFCTagUpdate(BaseModel):
    enabled_categories: Optional[List[ChallengeCategory]] = None


class NFCTagOut(BaseModel):
    id: int
    owner_id: int
    enabled_categories: str    # stored as comma-separated string
    health_score: int
    last_checkin: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NFCCheckin(BaseModel):
    """Sent when a user scans their NFC tag."""
    tag_owner_id: int          # whose tag was scanned


# ── Friendships ───────────────────────────────────────────────────────────────

class FriendRequest(BaseModel):
    addressee_username: str    # send request by username


class FriendRequestOut(BaseModel):
    id: int
    requester: UserPublic
    addressee: UserPublic
    status: FriendStatus
    created_at: datetime

    class Config:
        from_attributes = True


class FriendRequestAction(BaseModel):
    friendship_id: int
    action: str    # "accept" or "decline"


# ── Bets ──────────────────────────────────────────────────────────────────────

class BetCreate(BaseModel):
    opponent_username: str
    challenge_id: int
    wager: int


class BetOut(BaseModel):
    id: int
    challenger: UserPublic
    opponent: UserPublic
    challenge: ChallengeOut
    wager: int
    status: BetStatus
    winner: Optional[UserPublic] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BetAction(BaseModel):
    bet_id: int
    action: str    # "accept" or "decline"