from typing import Annotated

from clerk_backend_api import AuthenticateRequestOptions, authenticate_request
from clerk_backend_api.security.types import RequestState
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .core.config import Settings, get_settings

http_bearer = HTTPBearer(auto_error=False)


def require_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    _creds: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)] = None,
) -> str:
    if not settings.clerk_secret_key:
        raise HTTPException(
            status_code=503,
            detail="Clerk is not configured. Set CLERK_SECRET_KEY in backend/.env.",
        )

    state: RequestState = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.clerk_secret_key,
            authorized_parties=settings.authorized_parties,
            accepts_token=["session_token"],
        ),
    )

    if not state.is_signed_in:
        reason = state.reason.name if state.reason else "unauthorized"
        raise HTTPException(
            status_code=401,
            detail=f"Clerk authentication failed: {reason}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = state.payload.get("sub") if state.payload else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Authenticated Clerk user ID was not present in the session token.")
    return user_id
