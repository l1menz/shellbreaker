"""
Run this once to populate the database with starter challenges and badges.

Usage:
    cd backend
    python -m app.seed
"""

from .database import SessionLocal, engine
from . import models

# Create all tables
models.Base.metadata.create_all(bind=engine)


CHALLENGES = [
    # ── Easy / Greetings ──────────────────────────────────────────────────
    {
        "title": "Say Good Morning",
        "description": "Say good morning to a stranger today.",
        "instructions": "Make eye contact, smile, and say 'Good morning!' to someone you don't know.",
        "difficulty": models.DifficultyLevel.easy,
        "category": models.ChallengeCategory.greeting,
        "xp_reward": 10,
        "requires_partner": False,
    },
    {
        "title": "Hold the Door",
        "description": "Hold a door open for someone and say something kind.",
        "instructions": "Hold a door and add a warm comment like 'Have a great day!'",
        "difficulty": models.DifficultyLevel.easy,
        "category": models.ChallengeCategory.greeting,
        "xp_reward": 10,
        "requires_partner": False,
    },
    # ── Medium / Conversation ─────────────────────────────────────────────
    {
        "title": "Ask for a Recommendation",
        "description": "Ask a stranger to recommend their favourite café, book, or song.",
        "instructions": "Approach someone, apologise for interrupting, and ask for a recommendation. Thank them genuinely.",
        "difficulty": models.DifficultyLevel.medium,
        "category": models.ChallengeCategory.conversation,
        "xp_reward": 25,
        "requires_partner": False,
    },
    {
        "title": "Give a Genuine Compliment",
        "description": "Compliment a stranger on something specific — not just their appearance.",
        "instructions": "Find something real to compliment (a book they're reading, their bag, an action you noticed). Keep it natural.",
        "difficulty": models.DifficultyLevel.medium,
        "category": models.ChallengeCategory.conversation,
        "xp_reward": 25,
        "requires_partner": False,
    },
    {
        "title": "Start a Chat in a Queue",
        "description": "Strike up a conversation with the person next to you while waiting in line.",
        "instructions": "Comment on something you both share in context — the wait, the venue, the weather.",
        "difficulty": models.DifficultyLevel.medium,
        "category": models.ChallengeCategory.conversation,
        "xp_reward": 30,
        "requires_partner": False,
    },
    # ── Hard / Activity ───────────────────────────────────────────────────
    {
        "title": "Join a Table",
        "description": "Ask to sit with strangers at a café or food court and have a short chat.",
        "instructions": "Politely ask if the seat is free, introduce yourself, and aim for at least 2 minutes of conversation.",
        "difficulty": models.DifficultyLevel.hard,
        "category": models.ChallengeCategory.activity,
        "xp_reward": 50,
        "requires_partner": False,
    },
    {
        "title": "Organise a Spontaneous Plan",
        "description": "Invite an acquaintance (not a close friend) to do something today.",
        "instructions": "Text or call someone you rarely hang out with and suggest a specific activity right now.",
        "difficulty": models.DifficultyLevel.hard,
        "category": models.ChallengeCategory.activity,
        "xp_reward": 60,
        "requires_partner": False,
    },
    # ── Partner / NFC-ready ───────────────────────────────────────────────
    {
        "title": "ShellBreaker Handshake",
        "description": "Find another ShellBreaker user and complete a challenge together.",
        "instructions": "Tap phones to connect via NFC. Introduce yourselves and complete a greeting challenge together.",
        "difficulty": models.DifficultyLevel.medium,
        "category": models.ChallengeCategory.dare,
        "xp_reward": 40,
        "requires_partner": True,
    },
    {
        "title": "Two Truths and a Lie",
        "description": "Play Two Truths and a Lie with a stranger or fellow ShellBreaker.",
        "instructions": "Both players share three statements. Guess each other's lie. Shake on it to confirm completion.",
        "difficulty": models.DifficultyLevel.hard,
        "category": models.ChallengeCategory.dare,
        "xp_reward": 55,
        "requires_partner": True,
    },
]

BADGES = [
    {
        "name": "First Crack",
        "description": "Completed your very first challenge.",
        "challenge_count_threshold": 1,
    },
    {
        "name": "Shell Cracker",
        "description": "Completed 5 challenges.",
        "challenge_count_threshold": 5,
    },
    {
        "name": "Social Butterfly",
        "description": "Completed 20 challenges.",
        "challenge_count_threshold": 20,
    },
    {
        "name": "On Fire",
        "description": "Maintained a 7-day streak.",
        "streak_threshold": 7,
    },
    {
        "name": "Unstoppable",
        "description": "Maintained a 30-day streak.",
        "streak_threshold": 30,
    },
    {
        "name": "XP Hunter",
        "description": "Earned 500 XP.",
        "xp_threshold": 500,
    },
    {
        "name": "Shell Legend",
        "description": "Earned 2000 XP.",
        "xp_threshold": 2000,
    },
]


def seed():
    db = SessionLocal()
    try:
        # Challenges
        if db.query(models.Challenge).count() == 0:
            for data in CHALLENGES:
                db.add(models.Challenge(**data))
            print(f"✅ Seeded {len(CHALLENGES)} challenges.")
        else:
            print("⏭️  Challenges already seeded, skipping.")

        # Badges
        if db.query(models.Badge).count() == 0:
            for data in BADGES:
                db.add(models.Badge(**data))
            print(f"✅ Seeded {len(BADGES)} badges.")
        else:
            print("⏭️  Badges already seeded, skipping.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()