# SkillSensei Frontend

React + Vite + TypeScript frontend for SkillSensei.

## Run

```bash
npm install
copy .env.example .env
npm run dev
```

Set these frontend environment variables:

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
VITE_API_BASE_URL=http://localhost:8000/api
```

Authentication is handled by Supabase Auth. The frontend listens for Supabase auth state changes, persists the session, refreshes access tokens when needed, and sends the current access token to the FastAPI backend as a bearer token.

Google sign-in is supported when the Google provider is enabled in Supabase Authentication -> Providers and the deployed URL is configured as an allowed redirect URL.
