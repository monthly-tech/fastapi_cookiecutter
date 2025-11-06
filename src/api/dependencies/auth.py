from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.firebase_auth import FirebaseAuth

security = HTTPBearer()
firebase_auth = FirebaseAuth()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency that validates the Firebase ID token and returns the user claims.

    Args:
        credentials: The HTTP Authorization credentials containing the Bearer token

    Returns:
        dict: The decoded token claims containing user information

    Raises:
        HTTPException: If the token is invalid or missing
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = credentials.credentials
    return await firebase_auth.verify_token(token)
