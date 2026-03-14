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


# ─────────────────────────────────────────────
# Challenge schemas
# ─────────────────────────────────────────────
class ChallengeBase(BaseModel):
    title: str
    description: str
    instructions: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.easy
    category: ChallengeCategory = ChallengeCategory.greeting
    xp_reward: int = 10
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
# Auth schemas
# ─────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None