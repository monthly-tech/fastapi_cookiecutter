import logging
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json

import requests

from core.settings import settings

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
firebase_app = None


class FirebaseAuth:
    """Firebase Authentication service for validating tokens."""

    def __init__(self):
        self.initialize_firebase()

    def initialize_firebase(self):
        """Initialize Firebase Admin SDK with service account credentials."""
        global firebase_app

        if firebase_app is not None:
            return

        try:
            # Try to load Firebase credentials from environment
            if settings.FIREBASE_SERVICE_ACCOUNT_PATH:
                # Load from file path
                cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
            elif settings.FIREBASE_SERVICE_ACCOUNT_JSON:
                # Load from JSON string (useful for CI/CD)
                service_account_info = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
                cred = credentials.Certificate(service_account_info)
            else:
                # Try default application credentials
                cred = credentials.ApplicationDefault()

            firebase_app = firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service is not available"
            )

    async def verify_token(self, token: str) -> dict:
        """
        Verify a Firebase ID token and return the decoded claims.

        Args:
            token: The Firebase ID token to verify

        Returns:
            The decoded token claims

        Raises:
            HTTPException: If the token is invalid, expired, or revoked
        """
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(token, check_revoked=True)
            return decoded_token

        except ExpiredIdTokenError:
            logger.warning("Expired Firebase token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except RevokedIdTokenError:
            logger.warning("Revoked Firebase token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except InvalidIdTokenError as e:
            logger.warning(f"Invalid Firebase token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except Exception as e:
            logger.error(f"Error verifying Firebase token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error validating authentication"
            )

    async def get_user(self, uid: str) -> Optional[auth.UserRecord]:
        """
        Get user details from Firebase by UID.

        Args:
            uid: The Firebase user ID

        Returns:
            The user record or None if not found
        """
        try:
            user = auth.get_user(uid)
            return user
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error getting user from Firebase: {e}")
            return None


# Create a single instance of FirebaseAuth
firebase_auth = FirebaseAuth()

# Security scheme for Swagger UI
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get the current authenticated user from Firebase token.

    Args:
        credentials: The HTTP Bearer credentials containing the token

    Returns:
        The decoded token claims including user information

    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the token and get user claims
    user_claims = await firebase_auth.verify_token(credentials.credentials)

    # Optionally, get additional user details from Firebase
    user_record = await firebase_auth.get_user(user_claims["uid"])

    # Return user information
    return {
        "uid": user_claims["uid"],
        "email": user_claims.get("email"),
        "email_verified": user_claims.get("email_verified", False),
        "name": user_claims.get("name"),
        "picture": user_claims.get("picture"),
        "custom_claims": user_claims.get("custom_claims", {}),
        "firebase_user": user_record,
        "token_claims": user_claims
    }


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    Optional dependency for endpoints that can work with or without authentication.

    Args:
        credentials: The optional HTTP Bearer credentials

    Returns:
        The user information if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


async def exchange_custom_token_for_id_token(external_id: str) -> Optional[str]:
    """
    Exchange a Firebase custom token for an ID token.

    Args:
        api_key (str): The Firebase Console API key
        custom_token (str): The custom token received from Firebase Admin SDK

    Returns:
        Optional[str]: The Firebase ID token if successful, None if it fails
    """
    custom_token = auth.create_custom_token(external_id).decode()
    print('🔄 Exchanging custom token for Firebase ID token...')

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={settings.FIREBASE_API_KEY}"

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        'token': custom_token,
        'returnSecureToken': True,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            raise requests.exceptions.HTTPError(f"HTTP error! status: {response.status_code}")

        data = response.json()
        id_token = data.get('idToken')  # ✅ This is the authentication token

        print(f'🟢 Firebase ID Token: {id_token}')
        # Use this token in headers: Authorization: Bearer <id_token>

        return id_token

    except requests.exceptions.RequestException as error:
        print(f'❌ Error when exchanging custom token: {error}')
        return None
    except json.JSONDecodeError as error:
        print(f'❌ Error decoding JSON response: {error}')
        return None
