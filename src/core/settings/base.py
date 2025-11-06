import os
from pathlib import Path
from typing import List

from core.utils.environment import Environment
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from core.utils.envs import get_envs_files_path


ENVIRONMENT = os.environ.get("ENVIRONMENT")
Environment.check_value(ENVIRONMENT)


# For more information about settings standard check
# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENVIRONMENT: Environment = ENVIRONMENT

    PROJECT_NAME: str = "Monthly Onboarding Microservice"
    API_V1: str = "/api/v1"
    PROJECT_DIR: Path = Path(__file__).parent.parent.parent

    # API Settings
    # ----------------------------------------------------------------
    BACKEND_CORS_ORIGINS: List = ["*"]
    CORS_ALLOWED_ORIGINS: list = ["*"]
    DEFAULT_PAGE_SIZE: int = 50
    DEFAULT_ORDER_FIELD: str = "-created"

    # Scalar settings
    # --------------------------------------------------------------------------
    SCALAR_API_KEY: str = (
        ""  # Opcional: Can change it to use Scalar API (https://www.scalar.app/
    )

    # Date settings
    # --------------------------------------------------------------------------
    DATE_FORMAT: str = "%Y-%m-%d"
    DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    TIME_ZONE: str = "America/Mexico_City"

    # Database settings
    # --------------------------------------------------------------------------
    POSTGRESQL_URL: PostgresDsn = None

    # Only for cloudsql connection
    DB_USER: str = None
    DB_PASSWORD: str = None
    DB_NAME: str = None
    INSTANCE_UNIX_SOCKET: str = None

    # API Key configuration
    # --------------------------------------------------------------------------
    API_KEY: str = None

    # Google Cloud configuration
    # --------------------------------------------------------------------------
    GCP_PROJECT_ID: str = None
    GOOGLE_CLOUD_PROJECT: str = None
    GOOGLE_APPLICATION_CREDENTIALS: str | None   # Path to file with credentials
    GCP_MONTHLY_PROVIDERS_SECRET_ID: str = None  # ID of provider secret in Secret Manager
    GCP_BUCKET_NAME: str = None  # Name of the Google Cloud Storage bucket

    # Google Cloud Services
    # --------------------------------------------------------------------------
    GCP_PROJECT_ID: str = None
    GCP_MONTHLY_PROVIDERS_SECRET_ID: str = None

    # email FastMail settings
    # --------------------------------------------------------------------------
    MAIL_SERVER: str | None = None
    MAIL_PORT: int | None = None
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_SSL_TLS: bool | None = None
    MAIL_STARTTLS: bool | None = None
    MAIL_FROM: str | None = None

    # Firebase Authentication settings
    # --------------------------------------------------------------------------
    FIREBASE_SERVICE_ACCOUNT_PATH: str | None = (
        None  # Path to service account JSON file
    )
    FIREBASE_SERVICE_ACCOUNT_JSON: str | None = (
        None  # JSON string of service account credentials
    )
    FIREBASE_AUTH_ENABLED: bool = True  # Enable/disable Firebase authentication
    FIREBASE_AUTH_EMULATOR_HOST: str | None = (
        None  # For local development with emulator
    )
    FIREBASE_API_KEY: str | None = None  # Firebase Web API Key for token exchange

    model_config = SettingsConfigDict(
        env_file=get_envs_files_path(ENVIRONMENT), case_sensitive=True
    )
