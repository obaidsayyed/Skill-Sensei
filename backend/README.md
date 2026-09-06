# SkillSensei Backend

FastAPI backend for SkillSensei.

## Run on Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

## Environment

```env
APP_ENV=development
FRONTEND_ORIGIN=http://localhost:5173
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVER_ONLY_SERVICE_ROLE_OR_SECRET_KEY
GEMINI_API_KEY=
```

Gemini is optional for the MVP; the backend has a deterministic fallback summary.

## Authentication + database

Supabase Auth owns user identity and sessions. The frontend sends the Supabase Auth access token as `Authorization: Bearer <token>`. The backend verifies that token against Supabase Auth and uses the returned Supabase Auth user UUID as the owner key for student data.

The Supabase service-role/secret key is backend-only and must never be placed in the React `.env` file.

Run `supabase_schema.sql` once in the Supabase SQL Editor. The script includes a migration for the earlier Clerk-named ownership columns and keeps the current database model under the generic `user_id` field.

## Assessment question bank

SkillSensei includes a 15-question assessment after onboarding. The live assessment does not call Gemini. Questions are selected from the predefined bank stored in Supabase, with 15 questions available for each onboarding interest (150 seeded questions total). The backend keeps scoring metadata server-side and returns only question text/options to the browser.

The assessment result compares the student's answer pattern with their stated interests and labels the result as strong alignment, partial alignment, or a broadened view. Assessment-derived stream directions are explicitly tagged in the UI.
