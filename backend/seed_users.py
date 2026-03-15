"""
Seed predefined users from data/users.json into the database.
Run from backend directory:
    python seed_users.py
"""
import json
import os

# Load .env before importing app (which needs DATABASE_URL)
from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal, engine
from app import models

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def seed_users():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        with open(USERS_FILE) as f:
            users_data = json.load(f)

        for u in users_data:
            existing = db.query(models.User).filter(models.User.username == u["username"]).first()
            if existing:
                print(f"  User '{u['username']}' already exists. Skipping.")
                continue
            # Use pre-computed hash from JSON, or fall back to bcrypt hash of password
            hashed = u.get("hashed_password")
            if not hashed:
                import bcrypt
                hashed = bcrypt.hashpw(u["password"].encode(), bcrypt.gensalt()).decode()
            user = models.User(
                username=u["username"],
                email=u["email"],
                hashed_password=hashed,
                display_name=u.get("display_name"),
                coins=u.get("coins", 100),
            )
            db.add(user)
            print(f"  Created user: {u['username']} (coins={u.get('coins', 100)})")

        db.commit()
        print(f"✅ Seeded users from {USERS_FILE}")
    except FileNotFoundError:
        print(f"❌ {USERS_FILE} not found. Create it with predefined users.")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
