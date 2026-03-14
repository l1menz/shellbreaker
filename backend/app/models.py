from sqlalchemy import (
    Column, Integer, String, Boolean, Float,
    DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base


class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class ChallengeCategory(str, enum.Enum):
    greeting = "greeting"
    conversation = "conversation"
    activity = "activity"
    dare = "dare"


# ─────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String(80), nullable=True)
    avatar_url = Column(String, nullable=True)

    # Gamification
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)           # consecutive days active
    longest_streak = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    progress = relationship("UserChallengeProgress", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# Challenges
# ─────────────────────────────────────────────
class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)        # step-by-step guide
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.easy)
    category = Column(Enum(ChallengeCategory), default=ChallengeCategory.greeting)
    xp_reward = Column(Integer, default=10)
    requires_partner = Column(Boolean, default=False)  # NFC / two-player challenges
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    progress = relationship("UserChallengeProgress", back_populates="challenge")


# ─────────────────────────────────────────────
# User ↔ Challenge progress (join table + status)
# ─────────────────────────────────────────────
class ChallengeStatus(str, enum.Enum):
    assigned = "assigned"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"


class UserChallengeProgress(Base):
    __tablename__ = "user_challenge_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.assigned)
    partner_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # for NFC challenges
    note = Column(Text, nullable=True)                 # optional user reflection
    xp_earned = Column(Integer, default=0)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="progress")
    challenge = relationship("Challenge", back_populates="progress")
    partner = relationship("User", foreign_keys=[partner_user_id])


# ─────────────────────────────────────────────
# Badges
# ─────────────────────────────────────────────
class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String, nullable=True)
    xp_threshold = Column(Integer, nullable=True)      # awarded at this XP value
    streak_threshold = Column(Integer, nullable=True)  # awarded at this streak count
    challenge_count_threshold = Column(Integer, nullable=True)

    # Relationships
    users = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="users")