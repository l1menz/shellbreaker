# ShellBreaker

> Break out of your shell, one challenge at a time.

ShellBreaker is a gamified social app that helps people overcome social anxiety through daily real-world challenges; from simple greetings to full-on social dares. Earn XP, unlock badges, and level up your social confidence.

---

## The Idea

Modern life keeps us stuck in our own bubbles. ShellBreaker fights that by giving you a daily nudge, small, achievable social challenges that gradually push your comfort zone. Think of it like a fitness app, but for social skills.

Future features include NFC scanning to complete partner challenges with other ShellBreaker users in the real world.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | PostgreSQL + SQLAlchemy |
| Auth | JWT (via python-jose) |
| Deployment | Railway |

---

## Project Structure

```
shellbreaker/
├── frontend/          # React + Vite app
│   └── src/
│       ├── components/    # ChallengeCard, Leaderboard, NavBar, etc.
│       ├── pages/         # Home, Challenge, Profile, Login
│       ├── hooks/
│       └── services/      # API wrappers
│
└── backend/           # FastAPI app
    └── app/
        ├── main.py        # Entry point + CORS
        ├── database.py    # DB connection
        ├── models.py      # SQLAlchemy tables
        ├── schemas.py     # Pydantic models
        ├── seed.py        # Starter data
        └── routers/       # users, challenges, progress
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A PostgreSQL database (see below)

---

## Database Overview

| Table | Description |
|-------|-------------|
| `users` | Auth, XP, level, streak |
| `challenges` | Title, difficulty, category, XP reward, partner flag |
| `user_challenge_progress` | Tracks each user's challenge status |
| `badges` | Badge definitions with unlock thresholds |
| `user_badges` | Badges earned by each user |

Challenges have four categories (`greeting`, `conversation`, `activity`, `dare`) and three difficulty levels (`easy`, `medium`, `hard`). Partner challenges have a `requires_partner` flag ready for the NFC feature.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register a new user |
| GET | `/users/{id}` | Get user profile |
| GET | `/users/{id}/badges` | Get user badges |
| GET | `/users/leaderboard/top` | Top users by XP |
| GET | `/challenges/` | List all challenges |
| GET | `/challenges/daily` | Get today's challenge |
| GET | `/challenges/{id}` | Get a single challenge |
| POST | `/progress/assign` | Assign a challenge to a user |
| PATCH | `/progress/{id}` | Update progress / complete |
| GET | `/progress/user/{id}` | Get all progress for a user |

---

## Team

Built at UNIHACK by Rocket league pro squad.