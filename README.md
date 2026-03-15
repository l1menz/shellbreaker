# 🐚 ShellBreaker

> Break out of your shell, one challenge at a time.

ShellBreaker is a gamified social app that helps people overcome social anxiety through daily real-world challenges — from simple greetings to full-on social dares. Earn XP, unlock badges, and level up your social confidence.

---

## The Idea

Modern life keeps us stuck in our own bubbles. ShellBreaker fights that by giving you a daily nudge — small, achievable social challenges that gradually push your comfort zone. Think of it like a fitness app, but for social skills.

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

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Copy the example env file and fill in your database URL:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/shellbreaker
SECRET_KEY=your-secret-key-here
```

Seed the database with starter challenges and badges:

```bash
python -m app.seed
```

Start the server:

```bash
uvicorn app.main:app --reload
```

API will be running at `http://localhost:8000`. Visit `/docs` for the interactive Swagger UI.

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App will be running at `http://localhost:5173`.

---

### Local PostgreSQL (via Docker)

No Postgres installed? Spin one up with Docker:

```bash
docker compose up -d
```

`docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: shellbreaker
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpassword
    ports:
      - "5432:5432"
```

---

## Deploying to Railway

1. Push the repo to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Add a **PostgreSQL** plugin — Railway will auto-inject `DATABASE_URL`
4. Add your backend as a service pointing to the `backend/` directory
5. Add `SECRET_KEY` in the Railway environment variables
6. Deploy — Railway handles the rest

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

Built at [Hackathon Name] by [Your Team Name].