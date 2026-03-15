"""
Run this once to populate the database with starter challenges:
    python seed.py
"""
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.database import SessionLocal, engine
from app import models
from app.models import ChallengeCategory

models.Base.metadata.create_all(bind=engine)


def _ensure_columns():
    """Add tag_type and coin_reward if missing (for existing DBs)."""
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE challenges ADD COLUMN tag_type VARCHAR(32)"))
            conn.commit()
        except Exception:
            conn.rollback()
        try:
            conn.execute(text("ALTER TABLE challenges ADD COLUMN coin_reward INTEGER DEFAULT 0"))
            conn.commit()
        except Exception:
            conn.rollback()

# Map seed category strings to ChallengeCategory enum
CATEGORY_MAP = {
    "social": ChallengeCategory.greeting,
    "fitness": ChallengeCategory.activity,
    "career": ChallengeCategory.conversation,
    "skills": ChallengeCategory.activity,
}

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
    {
        "title": "Small talk starter",
        "description": "Start a conversation with someone in a queue or waiting room.",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Thank a stranger",
        "description": "Genuinely thank someone who helped you today (barista, driver, etc).",
        "difficulty": "easy",
        "category": "social",
        "points": 10,
    },
    {
        "title": "Ask for directions",
        "description": "Ask a stranger for directions even if you know the way.",
        "difficulty": "medium",
        "category": "social",
        "points": 20,
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
    {
        "title": "10k steps",
        "description": "Hit 10,000 steps in a single day.",
        "difficulty": "easy",
        "category": "fitness",
        "points": 15,
    },
    {
        "title": "Stretch session",
        "description": "Do 15 minutes of stretching or yoga.",
        "difficulty": "easy",
        "category": "fitness",
        "points": 10,
    },
    {
        "title": "Run 5km",
        "description": "Complete a 5km run or jog.",
        "difficulty": "medium",
        "category": "fitness",
        "points": 25,
    },
    {
        "title": "100 pushups",
        "description": "Complete 100 pushups in a day (can be in sets).",
        "difficulty": "medium",
        "category": "fitness",
        "points": 30,
    },
    {
        "title": "Gym PR",
        "description": "Hit a personal record on any lift or exercise.",
        "difficulty": "hard",
        "category": "fitness",
        "points": 50,
    },
    {
        "title": "Morning workout",
        "description": "Exercise before 8am.",
        "difficulty": "medium",
        "category": "fitness",
        "points": 25,
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
    {
        "title": "Update CV",
        "description": "Make one meaningful update to your CV or resume.",
        "difficulty": "easy",
        "category": "career",
        "points": 10,
    },
    {
        "title": "Apply for 3 jobs",
        "description": "Submit 3 job applications.",
        "difficulty": "medium",
        "category": "career",
        "points": 30,
    },
    {
        "title": "Learn one new thing",
        "description": "Spend 30 minutes learning a new work-related skill.",
        "difficulty": "easy",
        "category": "career",
        "points": 15,
    },
    {
        "title": "Networking event",
        "description": "Attend a networking event or meetup.",
        "difficulty": "hard",
        "category": "career",
        "points": 50,
    },
    {
        "title": "Mentor someone",
        "description": "Help someone else with a career or skill question.",
        "difficulty": "medium",
        "category": "career",
        "points": 35,
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
    {
        "title": "Read 20 pages",
        "description": "Read and absorb 20 pages of a book or article.",
        "difficulty": "easy",
        "category": "skills",
        "points": 10,
    },
    {
        "title": "Practice a skill",
        "description": "Spend 20 minutes deliberate practice on a skill.",
        "difficulty": "easy",
        "category": "skills",
        "points": 10,
    },
    {
        "title": "Teach someone",
        "description": "Explain a concept you know to someone.",
        "difficulty": "medium",
        "category": "skills",
        "points": 25,
    },
    {
        "title": "Build something small",
        "description": "Create a small project or prototype.",
        "difficulty": "hard",
        "category": "skills",
        "points": 60,
    },
]


def seed():
    _ensure_columns()
    db = SessionLocal()
    try:
        existing = db.query(models.Challenge).count()
        if existing > 0:
            print(f"Database already has {existing} challenges. Skipping seed.")
            return

        COIN_BY_DIFFICULTY = {"easy": 5, "medium": 15, "hard": 30}
        for data in CHALLENGES:
            row = {
                "title": data["title"],
                "description": data["description"],
                "difficulty": data["difficulty"],
                "category": CATEGORY_MAP.get(data["category"], ChallengeCategory.greeting),
                "tag_type": data["category"],  # fitness, social, career, skills
                "xp_reward": data.get("points", 10),
                "coin_reward": COIN_BY_DIFFICULTY.get(data["difficulty"], 5),
            }
            challenge = models.Challenge(**row)
            db.add(challenge)

        db.commit()
        print(f"✅ Seeded {len(CHALLENGES)} challenges into the database.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()