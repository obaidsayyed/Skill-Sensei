# SkillSensei Auth + Database Setup

## 1. Frontend

```bash
cd frontend
npm install
copy .env.example .env
```

Set:

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
VITE_API_BASE_URL=http://localhost:8000/api
```

The Clerk React SDK is `@clerk/react`. The app uses `ClerkProvider`, `Show`, `SignInButton`, `SignUpButton`, `UserButton`, and `useAuth()`.

## 2. Backend

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

Set:

```env
CLERK_SECRET_KEY=sk_test_...
CLERK_JWT_KEY=-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----
CLERK_AUTHORIZED_PARTIES=http://localhost:5173

SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY

GEMINI_API_KEY=YOUR_GEMINI_KEY
```

The Clerk JWT public key is available in Clerk Dashboard -> API Keys -> Show JWT public key. The backend uses Clerk's official `clerk-backend-api` authentication flow and verifies only `session_token` requests.

## 3. Supabase

Open the Supabase SQL Editor and run `backend/supabase_schema.sql` once.

The backend stores the student's SkillSensei profile, career recommendations, roadmap, and progress in the `students` table. Rows are owned by the verified Clerk `sub` value.

Do not put `SUPABASE_SERVICE_ROLE_KEY` in the frontend.

## 4. Run

Terminal 1:

```bash
cd backend
.venv\\Scripts\\activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173`.

## 5. Expected flow

Sign up with Clerk -> SkillSensei detects the authenticated Clerk user -> onboarding -> FastAPI verifies the Clerk session -> Supabase persists the student -> dashboard loads -> logout calls Clerk sign-out and returns to the landing page.

## 6. If Supabase is not configured yet

The backend has an in-memory fallback so the app can still be explored after Clerk is configured. Restarting the backend clears that fallback data. Configure Supabase before relying on persistence.
