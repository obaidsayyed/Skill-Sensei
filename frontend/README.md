# SkillSensei Frontend

React + Vite + TypeScript frontend for SkillSensei.

## Run

```bash
npm install
copy .env.example .env
npm run dev
```

The frontend expects the backend at:

`VITE_API_BASE_URL=http://localhost:8000/api`

## Fixed in this build

- Clerk now owns authentication, session state, and logout.
- Internal navigation uses React Router instead of full page reloads.
- Career detail back navigation stays inside the app.
- Dashboard, careers, roadmap, resources, progress, profile, and college actions now surface API errors instead of silently failing.
- Profile save refreshes derived recommendations through the backend.
- Student API requests automatically attach the Clerk session token.

## Clerk setup

Create `frontend/.env` from `.env.example` and set `VITE_CLERK_PUBLISHABLE_KEY` from your Clerk Dashboard. Clerk's current React SDK uses `@clerk/react`, `ClerkProvider`, `Show`, `SignInButton`, `SignUpButton`, `UserButton`, and `useAuth()` for session tokens and sign-out.

The frontend sends the Clerk session token as `Authorization: Bearer <token>` to the FastAPI backend.

See `../SETUP_AFTER_CLERK.md` in the project bundle for the exact Clerk + FastAPI setup sequence.
