"""
Run this once to populate the database with starter challenges:
    python seed.py
"""
from app.database import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

CHALLENGES = [
    # ── Social ────────────────────────────────────────────────────────────────
    {
        "title": "The Smile",
        "description": "Make genuine eye contact and smile at 3 strangers today.",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Say Good Morning",
        "description": "Say 'good morning' to someone you've never spoken to before.",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Compliment a Stranger",
        "description": "Give a genuine compliment to someone you don't know.",
        "difficulty": "easy",
        "category": "social",
        "points": 15,
    },
    {
        "title": "Ask for a Recommendation",
        "description": "Ask a stranger what their favourite coffee shop, restaurant or book is.",
        "difficulty": "medium",
        "category": "social",
        "points": 25,
    },
    {
        "title": "Join the Table",
        "description": "Ask to sit with strangers at a café or food court and strike up a conversation.",
        "difficulty": "hard",
        "category": "social",
        "points": 60,
    },
    {
        "title": "Spontaneous Plan",
        "description": "Exchange contact details with a stranger and make an actual plan to meet up.",
        "difficulty": "hard",
        "category": "social",
        "points": 75,
    },
    # ── Fitness ───────────────────────────────────────────────────────────────
    {
        "title": "Morning Mover",
        "description": "Do 20 minutes of exercise before 9am.",
        "difficulty": "easy",
        "category": "fitness",
        "points": 15,
    },
    {
        "title": "Cold Shower",
        "description": "Finish your shower with 60 seconds of cold water.",
        "difficulty": "medium",
        "category": "fitness",
        "points": 25,
    },
    {
        "title": "Stranger Workout",
        "description": "Ask someone at the gym or park to show you their workout routine.",
        "difficulty": "hard",
        "category": "fitness",
        "points": 50,
    },
    # ── Career ────────────────────────────────────────────────────────────────
    {
        "title": "LinkedIn Hello",
        "description": "Send a personalised connection request to someone whose work you admire.",
        "difficulty": "easy",
        "category": "career",
        "points": 15,
    },
    {
        "title": "Speak Up",
        "description": "Share an idea or opinion in a meeting or group setting you'd normally stay quiet in.",
        "difficulty": "medium",
        "category": "career",
        "points": 30,
    },
    {
        "title": "Cold Reach Out",
        "description": "Email or message someone senior in your field asking for a 15-minute chat.",
        "difficulty": "hard",
        "category": "career",
        "points": 65,
    },
    # ── Skills ────────────────────────────────────────────────────────────────
    {
        "title": "Learn One Thing",
        "description": "Spend 20 minutes learning a skill you've been putting off.",
        "difficulty": "easy",
        "category": "skills",
        "points": 10,
    },
    {
        "title": "Teach It",
        "description": "Explain something you know well to a person who doesn't — in person.",
        "difficulty": "medium",
        "category": "skills",
        "points": 30,
    },
    {
        "title": "Public Demo",
        "description": "Show something you've built or learned to a group of at least 3 people.",
        "difficulty": "hard",
        "category": "skills",
        "points": 60,
    },
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(models.Challenge).count()
        if existing > 0:
            print(f"Database already has {existing} challenges. Skipping seed.")
            return

        for data in CHALLENGES:
            challenge = models.Challenge(**data)
            db.add(challenge)

        db.commit()
        print(f"✅ Seeded {len(CHALLENGES)} challenges into the database.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()