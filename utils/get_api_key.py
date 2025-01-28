from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from core.config import settings

api_key_header = APIKeyHeader(name=settings.auth.api_key_name, auto_error=False)


def get_api_key(auth_header: str = Depends(api_key_header)):
    if auth_header == settings.auth.api_key:
        return auth_header
    raise HTTPException(
        status_code=403,
        detail="Could not validate API key"
    )
