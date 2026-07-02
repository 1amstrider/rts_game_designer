# Deployment Guide

## Deploy to Hugging Face Spaces

### 1. Prerequisites
- Hugging Face account: https://huggingface.co/join
- Supabase project: https://supabase.com
- Cloudinary account: https://cloudinary.com

### 2. Supabase Setup

1. Create a new Supabase project
2. Go to **SQL Editor** → **New query**
3. Copy-paste the contents of `database/schema.sql`
4. Click **Run**
5. Go to **Project Settings** → **API**:
   - Copy `Project URL` → set as `SUPABASE_URL` in HF Spaces secrets
   - Copy `anon public` API key → set as `SUPABASE_KEY`

### 3. Cloudinary Setup

1. Sign up at https://cloudinary.com
2. Go to **Dashboard**:
   - Copy `Cloud name` → set as `CLOUDINARY_CLOUD_NAME`
   - Go to **Settings** → **Security** → **API Keys**:
     - Copy `API Key` → set as `CLOUDINARY_API_KEY`
     - Copy `API Secret` → set as `CLOUDINARY_API_SECRET`

### 4. Hugging Face Spaces Deployment

1. Go to https://huggingface.co/spaces
2. Click **Create new Space**
3. Fill in:
   - **Owner**: Your username
   - **Space name**: `rts-game-designer` (or whatever)
   - **License**: `apache-2.0`
   - **Space SDK**: `Docker`
   - **Space hardware**: `CPU basic` (free tier)
   - **Visibility**: `Public` or `Private`
4. Click **Create Space**
5. In the Space settings, go to **Repository** → upload files OR use Git:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/rts-game-designer
   cd rts-game-designer
   # Copy all files from this project
   cp -r /path/to/rts_game_designer/* .
   git add .
   git commit -m "Initial deployment"
   git push
   ```

### 5. Set Environment Variables (Secrets)

In your HF Space → **Settings** → **Secrets**:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://your-project.supabase.co` |
| `SUPABASE_KEY` | `eyJhbG...` (anon key) |
| `CLOUDINARY_CLOUD_NAME` | `your_cloud_name` |
| `CLOUDINARY_API_KEY` | `123456789` |
| `CLOUDINARY_API_SECRET` | `your_secret` |

These are encrypted and never exposed in the UI or logs.

### 6. Verify Deployment

1. Wait for the Space to build (green dot)
2. Open the Space URL
3. Click **Design Docs** → you should see the documents
4. Click **Editor** → select a Kingdom → you should see heroes

### 7. Local Development

For local development without Supabase/Cloudinary, just don't set the env vars:

```bash
# .env (not committed, already in .gitignore)
# Leave empty for local mode
```

The app will fall back to local Excel + file storage.

### 8. Data Migration

To migrate existing local data to Supabase:

```bash
python scripts/migrate_to_supabase.py
```

(This script will be created if needed.)

---

## Architecture

```
Hugging Face Spaces (Docker)
├── FastAPI app (app.py)
├── Supabase Client (database/supabase_client.py)
├── Cloudinary Service (services/cloudinary_service.py)
├── Local Fallback (when env vars not set)
└── GitHub Integration (design docs versioning)

Data Flow:
1. User opens HF Space URL
2. App loads heroes from Supabase Postgres
3. Images loaded from Cloudinary URLs
4. Design docs loaded from local files (Git-tracked)
5. Changes saved to Supabase + Cloudinary
6. Design doc changes auto-committed to Git
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| App shows "No heroes" | Check SUPABASE_URL and SUPABASE_KEY are set correctly |
| Images don't upload | Check Cloudinary credentials and folder permissions |
| Can't save design docs | Git must be configured in the container (already in Dockerfile) |
| Build fails | Check `requirements.txt` has all dependencies |

## Security Notes

- `.env` is in `.gitignore` — never commit credentials
- HF Spaces Secrets are encrypted at rest
- Supabase uses Row Level Security (RLS) — currently open for ease of use
- For production, enable Supabase Auth and update RLS policies
