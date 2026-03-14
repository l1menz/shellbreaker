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
        "title": "Corner mouth peaking",
        "description": "Make genuine eye contact and smile at 3 strangers today.",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Good Morning!",
        "description": "Say 'good morning' to someone you've never spoken to before.",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Compliments abound",
        "description": "Give a genuine compliment to someone you don't know.",
        "difficulty": "easy",
        "category": "social",
        "points": 15,
    },
    {
        "title": "Stragner's Recommendation",
        "description": "Ask a stranger what their favourite coffee shop, restaurant or book is.",
        "difficulty": "medium",
        "category": "social",
        "points": 25,
    },
    {
        "title": "Epic table crasher",
        "description": "Ask to sit with strangers at a café or food court and strike up a conversation.",
        "difficulty": "hard",
        "category": "social",
        "points": 60,
    },
    {
        "title": "Unplanned rendezvous",
        "description": "Exchange contact details with a stranger and make an actual plan to meet up.",
        "difficulty": "hard",
        "category": "social",
        "points": 75,
    },
    # ── Fitness ───────────────────────────────────────────────────────────────
    {
        "title": "Early bird gets the worm",
        "description": "Do 20 minutes of exercise before 9am.",
        "difficulty": "easy",
        "category": "fitness",
        "points": 15,
    },
    {
        "title": "Cold plunge",
        "description": "Finish your shower with 60 seconds of cold water.",
        "difficulty": "medium",
        "category": "fitness",
        "points": 25,
    },
    {
        "title": "Gmybros unite",
        "description": "Ask someone at the gym or park to show you their workout routine, and join them if they are willing",
        "difficulty": "hard",
        "category": "fitness",
        "points": 50,
    },
    # ── Career ────────────────────────────────────────────────────────────────
    {
        "title": "LinkedIn warrior",
        "description": "Send a personalised connection request to someone whose work you admire.",
        "difficulty": "easy",
        "category": "career",
        "points": 15,
    },
    {
        "title": "Big man at the table",
        "description": "Share an idea or opinion in a meeting or group setting you'd normally stay quiet in.",
        "difficulty": "medium",
        "category": "career",
        "points": 30,
    },
    {
        "title": "Stone cold reachout",
        "description": "Email or message someone senior in your field asking for a coffee chat.",
        "difficulty": "hard",
        "category": "career",
        "points": 65,
    },
    # ── Skills ────────────────────────────────────────────────────────────────
    {
        "title": "Skills for thrills",
        "description": "Spend 20 minutes learning a skill you've been putting off.",
        "difficulty": "easy",
        "category": "skills",
        "points": 10,
    },
    {
        "title": "Call me Professor",
        "description": "Explain something you know well to a person who doesn't — in person.",
        "difficulty": "medium",
        "category": "skills",
        "points": 30,
    },
    {
        "title": "Tech bro standup",
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