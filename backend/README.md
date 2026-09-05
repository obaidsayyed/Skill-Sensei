# SkillSensei Backend

FastAPI backend for SkillSensei.

## Run on Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Environment

```env
GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
CLERK_SECRET_KEY=
CLERK_JWT_KEY=
CLERK_AUTHORIZED_PARTIES=http://localhost:5173
```

Gemini is optional for the MVP; the backend has a deterministic fallback summary.

## Fixed in this build

- Profile updates invalidate cached career recommendations and roadmap data.
- Roadmap completion and college prediction remain API-backed.

## Clerk + Supabase setup

Create `backend/.env` from `.env.example`.

Set `CLERK_SECRET_KEY` and `CLERK_JWT_KEY` from Clerk Dashboard. `CLERK_JWT_KEY` is the PEM public key under API Keys -> Show JWT public key. Set `CLERK_AUTHORIZED_PARTIES` to the exact frontend origins that should be allowed, for example `http://localhost:5173`.

Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` for persistence. Run `supabase_schema.sql` once in the Supabase SQL editor.

The backend verifies the Clerk session token before any student-specific API operation and uses the verified Clerk `sub` as the owner key. The Supabase service-role key is backend-only and must never be placed in the React `.env` file.

See `../SETUP_AFTER_CLERK.md` in the project bundle for the exact Clerk + Supabase setup sequence.

## Assessment question bank

SkillSensei now includes a 15-question assessment after onboarding. The live assessment does not call Gemini. Questions are selected from a predefined bank stored in Supabase, with 15 questions available for each onboarding interest (150 seeded questions total). The backend keeps the scoring metadata server-side and returns only the question text/options to the browser.

Run `supabase_schema.sql` in the Supabase SQL editor to create the `assessment_questions` and `assessment_attempts` tables and seed the full question bank. The assessment result compares the student's answer pattern with their stated interests and labels the result as strong alignment, partial alignment, or a broadened view. Assessment-derived stream directions are explicitly tagged in the UI.
