from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .core.config import Settings, get_settings

http_bearer = HTTPBearer(auto_error=False)


def require_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)] = None,
) -> str:
    """Verify a Supabase Auth access token and return the authenticated user UUID."""
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise HTTPException(
            status_code=503,
            detail="Supabase Auth is not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in backend/.env.",
        )

    if not creds or creds.scheme.lower() != "bearer" or not creds.credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Sign in to SkillSensei.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    url = f"{settings.supabase_url.rstrip('/')}/auth/v1/user"
    headers = {
        "apikey": settings.supabase_service_role_key,
        "Authorization": f"Bearer {creds.credentials}",
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(url, headers=headers)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Supabase Auth could not be reached.") from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=401,
            detail="Supabase session is invalid or expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Supabase returned an invalid user response.") from exc

    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Authenticated Supabase user ID was not present.")

    return str(user_id)
