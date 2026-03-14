from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


# ── Enums ─────────────────────────────────────────────────────────────────────

class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class ChallengeStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    skipped = "skipped"


class ChallengeCategory(str, enum.Enum):
    social = "social"
    fitness = "fitness"
    career = "career"
    skills = "skills"


class FriendStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"


class BetStatus(str, enum.Enum):
    open = "open"          # waiting for opponent to accept
    active = "active"      # both accepted, in progress
    completed = "completed"
    cancelled = "cancelled"


# ── Core models ───────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    coins = Column(Integer, default=100)    # in-game currency for betting
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    challenge_attempts = relationship("UserChallenge", back_populates="user")
    nfc_tag = relationship("NFCTag", back_populates="owner", uselist=False)

    sent_requests = relationship(
        "Friendship", foreign_keys="Friendship.requester_id", back_populates="requester"
    )
    received_requests = relationship(
        "Friendship", foreign_keys="Friendship.addressee_id", back_populates="addressee"
    )

    bets_initiated = relationship("Bet", foreign_keys="Bet.challenger_id", back_populates="challenger")
    bets_received = relationship("Bet", foreign_keys="Bet.opponent_id", back_populates="opponent")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    category = Column(Enum(ChallengeCategory), nullable=False)
    points = Column(Integer, nullable=False)    # XP reward on completion

    attempts = relationship("UserChallenge", back_populates="challenge")
    bets = relationship("Bet", back_populates="challenge")


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.pending)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    assigned_date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="challenge_attempts")
    challenge = relationship("Challenge", back_populates="attempts")


# ── NFC Tag ───────────────────────────────────────────────────────────────────

class NFCTag(Base):
    """
    Represents a physical NFC sticker owned by a user.
    Stores their preferred challenge categories and a health score
    that updates each time the tag is scanned/checked in.
    """
    __tablename__ = "nfc_tags"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Comma-separated list of enabled categories e.g. "social,fitness"
    # Kept simple to avoid a join table for the MVP
    enabled_categories = Column(String, default="social")

    health_score = Column(Integer, default=100)   # 0–100, decays without check-ins
    last_checkin = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="nfc_tag")


# ── Friendships ───────────────────────────────────────────────────────────────

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(FriendStatus), default=FriendStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_requests")
    addressee = relationship("User", foreign_keys=[addressee_id], back_populates="received_requests")


# ── Bets ──────────────────────────────────────────────────────────────────────

class Bet(Base):
    """
    One user challenges another on a specific challenge.
    Both wager coins. The first to complete wins the pot.
    """
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    challenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)

    wager = Column(Integer, nullable=False)         # coins each side puts in
    status = Column(Enum(BetStatus), default=BetStatus.open)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    challenger = relationship("User", foreign_keys=[challenger_id], back_populates="bets_initiated")
    opponent = relationship("User", foreign_keys=[opponent_id], back_populates="bets_received")
    challenge = relationship("Challenge", back_populates="bets")
    winner = relationship("User", foreign_keys=[winner_id])