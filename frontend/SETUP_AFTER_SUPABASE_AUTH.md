# SkillSensei Supabase Auth + Database Setup

## 1. Supabase

Create a Supabase project and run `../backend/supabase_schema.sql` in the SQL Editor.

In Authentication -> Providers, enable the providers you want. The frontend includes email/password and Google sign-in.

Set the Supabase Auth Site URL and redirect URLs for the environment you are running, for example:

```text
http://localhost:5173
```

For production, add the exact production frontend URL as an allowed redirect URL.

## 2. Frontend

```bash
cd frontend
npm install
copy .env.example .env
```

Set:

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
VITE_API_BASE_URL=http://localhost:8000/api
```

The publishable key is safe for the browser. Never put the server-only service-role/secret key in the frontend.

## 3. Backend

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

Set:

```env
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVER_ONLY_SERVICE_ROLE_OR_SECRET_KEY
FRONTEND_ORIGIN=http://localhost:5173
GEMINI_API_KEY=
```

The FastAPI auth dependency validates the Supabase Auth access token against the Supabase Auth `/auth/v1/user` endpoint and uses the returned Supabase user UUID as ownership identity.

## 4. Run

Terminal 1:

```bash
cd backend
.venv\\Scripts\\activate
python -m uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173`.

## 5. Expected flow

Create account / sign in with Supabase Auth -> SkillSensei detects the Supabase session -> onboarding -> FastAPI verifies the Supabase access token -> Supabase persists the student -> dashboard loads -> logout signs out of Supabase and returns to the landing page.
