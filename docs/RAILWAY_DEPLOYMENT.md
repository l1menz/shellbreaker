# Railway Deployment Guide

Deploy ShellBreaker to Railway for NFC URL tags. Railway provides a public domain for each service.

## Prerequisites

- [Railway account](https://railway.app)
- GitHub repo connected to Railway

## Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app) and create a new project
2. Add **PostgreSQL** from the plugin catalog (this creates a database service)

## Step 2: Deploy Backend

1. Click **+ New** → **GitHub Repo** → select your repo
2. Configure the backend service:
   - **Root Directory**: `backend`
   - **Dockerfile Path**: `Dockerfile` (auto-detected)
3. **Link the database** – In the backend service, go to **Variables** → **+ New Variable** → **Add Reference**:
   - Variable: `DATABASE_URL`
   - Reference: Select your **PostgreSQL** service → `DATABASE_URL`
   - (This injects the database connection string into your backend)
4. Add **Variables**:
   - `SECRET_KEY` – generate a random string (e.g. `openssl rand -hex 32`)
   - `CORS_ORIGINS` – leave empty for now; we'll set it after frontend deploys
5. Under **Settings** → **Networking** → enable **Generate Domain**
6. Deploy and copy the generated URL (e.g. `https://unihack-2026-backend.up.railway.app`)

## Step 3: Deploy Frontend

1. Click **+ New** → **GitHub Repo** → select the same repo
2. Configure the frontend service:
   - **Root Directory**: `frontend`
   - **Dockerfile Path**: `Dockerfile`
3. Add **Variables**:
   - `VITE_API_BASE_URL` – your backend Railway URL (e.g. `https://unihack-2026-backend.up.railway.app`)
4. Under **Settings** → **Networking** → enable **Generate Domain**
5. Deploy and copy the frontend URL (e.g. `https://unihack-2026-frontend.up.railway.app`)

## Step 4: Update Backend CORS

1. Go back to the **backend** service
2. Add/update variable: `CORS_ORIGINS` = your frontend URL (e.g. `https://unihack-2026-frontend.up.railway.app`)
3. Redeploy the backend

## Step 5: Seed the Database (one-time)

Run the seed script to populate challenges. From your machine:

```bash
cd backend
# Set DATABASE_URL to your Railway Postgres URL (from Railway dashboard → PostgreSQL → Connect)
export DATABASE_URL="postgresql://user:pass@host:port/railway"
export SECRET_KEY="your-secret-key"
python3 seed.py
```

Or use Railway's **Run Command** in the backend service (if available), or connect via `railway run`.

## NFC URL Tags

Use your **frontend** Railway domain for NFC stickers:

| Tag Type | URL |
|----------|-----|
| Fitness | `https://YOUR-FRONTEND-URL.up.railway.app/scan?tag_type=fitness` |
| Social  | `https://YOUR-FRONTEND-URL.up.railway.app/scan?tag_type=social` |
| Career  | `https://YOUR-FRONTEND-URL.up.railway.app/scan?tag_type=career` |
| Skills  | `https://YOUR-FRONTEND-URL.up.railway.app/scan?tag_type=skills` |

Short URLs (for small NFC tags):

- `https://YOUR-FRONTEND-URL.up.railway.app/f`
- `https://YOUR-FRONTEND-URL.up.railway.app/s`
- `https://YOUR-FRONTEND-URL.up.railway.app/c`
- `https://YOUR-FRONTEND-URL.up.railway.app/k`

## Environment Variables Summary

### Backend
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Auto-set by Railway PostgreSQL |
| `SECRET_KEY` | Yes | JWT signing key |
| `CORS_ORIGINS` | Yes | Frontend URL (comma-separated for multiple) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Default: 1440 (24h) |

### Frontend
| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | Yes | Backend API URL (must be set at build time) |

## Troubleshooting

### "DATABASE_URL environment variable is not set" / Container crashes on start

The backend needs `DATABASE_URL` from your PostgreSQL database. Add it as a **variable reference**:

1. Open your **backend** service in Railway
2. Go to **Variables** tab
3. Click **+ New Variable** → **Add Reference**
4. Variable name: `DATABASE_URL`
5. Select your **PostgreSQL** service → `DATABASE_URL`
6. Save – Railway will redeploy automatically

### Manual DATABASE_URL (alternative)

If "Add Reference" isn't available, copy the URL manually:

1. Click your **PostgreSQL** service
2. Go to **Connect** or **Variables** tab
3. Copy the `DATABASE_URL` value (starts with `postgresql://` or `postgres://`)
4. In your **backend** service → Variables → Add: `DATABASE_URL` = (paste the value)

## Local Docker Test (optional)

```bash
# Backend (requires DATABASE_URL)
cd backend && docker build -t shellbreaker-backend . && docker run -p 8000:8000 -e DATABASE_URL=postgresql://... -e SECRET_KEY=dev -e CORS_ORIGINS=http://localhost:5173 shellbreaker-backend

# Frontend
cd frontend && docker build -t shellbreaker-frontend --build-arg VITE_API_BASE_URL=http://localhost:8000 . && docker run -p 80:80 shellbreaker-frontend
```
