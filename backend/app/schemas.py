from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import DifficultyLevel, ChallengeCategory, ChallengeStatus


# ─────────────────────────────────────────────
# User schemas
# ─────────────────────────────────────────────
class UserBase(BaseModel):
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserPublic(UserBase):
    id: int
    xp: int
    level: int
    streak: int
    longest_streak: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserOut(UserPublic):
    """
    Backwards-compatible alias for older code that expects `UserOut`.
    Currently identical to `UserPublic`.
    """
    pass


# ─────────────────────────────────────────────
# Challenge schemas
# ─────────────────────────────────────────────
class ChallengeBase(BaseModel):
    title: str
    description: str
    instructions: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.easy
    category: ChallengeCategory = ChallengeCategory.greeting
    tag_type: Optional[str] = None
    xp_reward: int = 10
    coin_reward: int = 0
    requires_partner: bool = False


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeOut(ChallengeBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Progress schemas
# ─────────────────────────────────────────────
class ProgressCreate(BaseModel):
    challenge_id: int
    partner_user_id: Optional[int] = None


class ProgressUpdate(BaseModel):
    status: ChallengeStatus
    note: Optional[str] = None


class ProgressOut(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    status: ChallengeStatus
    partner_user_id: Optional[int]
    note: Optional[str]
    xp_earned: int
    assigned_at: datetime
    completed_at: Optional[datetime]
    challenge: ChallengeOut

    class Config:
        from_attributes = True


# Backwards-compatible alias for older code that expects `UserChallengeOut`.
class UserChallengeOut(ProgressOut):
    pass


# ─────────────────────────────────────────────
# Badge schemas
# ─────────────────────────────────────────────
class BadgeOut(BaseModel):
    id: int
    name: str
    description: str
    icon_url: Optional[str]
    awarded_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# NFC schemas
# ─────────────────────────────────────────────
class NFCTagCreate(BaseModel):
    enabled_categories: list[ChallengeCategory]


class NFCTagUpdate(BaseModel):
    enabled_categories: Optional[list[ChallengeCategory]] = None


class NFCTagOut(BaseModel):
    id: int
    owner_id: int
    enabled_categories: str
    last_checkin: Optional[datetime]
    health_score: int

    class Config:
        from_attributes = True


class NFCCheckin(BaseModel):
    tag_owner_id: int


class NFCTagScan(BaseModel):
    """Body for scanning an NFC tag to load its challenges."""
    tag_type: str  # "fitness", "social", "career", "skills"


# ─────────────────────────────────────────────
# Auth schemas
# ─────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


class CompleteChallenge(BaseModel):
    """Body for marking a user challenge as completed."""
    user_challenge_id: int