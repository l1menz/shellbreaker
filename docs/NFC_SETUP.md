# NFC URL Setup for ShellBreaker

This guide explains how to program NFC stickers so that when users scan them, they open the app and load the corresponding challenges.

## NFC URL Format

Each NFC sticker should be programmed with a URL in this format:

```
https://YOUR_DOMAIN/scan?tag_type=TAG_TYPE
```

Replace:
- **YOUR_DOMAIN** – Your deployed frontend URL (e.g. `shellbreaker.app` or `unihack.example.com`)
- **TAG_TYPE** – One of: `fitness`, `social`, `career`, `skills`

### Example URLs

| Tag Type | Full URL | Short URL (for small NFC tags) |
|----------|----------|-------------------------------|
| Fitness  | `https://shellbreaker.app/scan?tag_type=fitness` | `https://shellbreaker.app/f` |
| Social   | `https://shellbreaker.app/scan?tag_type=social`  | `https://shellbreaker.app/s` |
| Career   | `https://shellbreaker.app/scan?tag_type=career`  | `https://shellbreaker.app/c` |
| Skills   | `https://shellbreaker.app/scan?tag_type=skills`  | `https://shellbreaker.app/k` |

## How It Works

1. **User scans NFC sticker** → Phone opens the URL in the browser
2. **If logged in** → App loads challenges for that tag type and redirects to home
3. **If not logged in** → User is prompted to log in or register, then redirected back to complete the scan

## Programming NFC Stickers

### Option 1: NFC Tools App (Android)

1. Install [NFC Tools](https://play.google.com/store/apps/details?id=com.wakdev.wdnfc) or similar
2. Open the app → **Write** tab
3. Add a record → **URL/URI**
4. Enter the full URL (e.g. `https://yoursite.com/scan?tag_type=fitness`)
5. Tap **Write** and hold the sticker to the back of your phone

### Option 2: NFC TagWriter (iOS)

1. Install [NFC TagWriter by NXP](https://apps.apple.com/app/nfc-tagwriter-by-nxp/id1246143256)
2. Create new record → **URL**
3. Enter the URL
4. Write to your NFC sticker

### Option 3: Short URLs (for tags with limited storage)

Some NFC tags have limited storage (~48 bytes for basic tags). Use the short paths:

- `/f` = fitness
- `/s` = social  
- `/c` = career
- `/k` = skills

Example: `https://shellbreaker.app/f` (saves ~20 characters vs full URL)

## Deployment

For Railway deployment (recommended for NFC), see [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md).

## Tag Types & Challenges

Each tag type maps to a set of challenges in the database:

- **fitness** – Gym, running, exercise challenges
- **social** – Talk to strangers, connect with people
- **career** – Networking, job applications
- **skills** – Learn, teach, build

Challenges are seeded in `backend/seed.py` and must have `tag_type` set to match.

## Testing Locally

1. Use your local URL: `http://localhost:5173/scan?tag_type=fitness`
2. Or use your machine's LAN IP for testing on a real phone: `http://192.168.1.x:5173/scan?tag_type=fitness`
3. Ensure backend is running and CORS allows your frontend origin
