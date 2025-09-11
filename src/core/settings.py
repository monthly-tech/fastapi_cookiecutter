import json
from pathlib import Path
from typing import List

from google.cloud import bigquery
from google.oauth2 import service_account
from pydantic_settings import BaseSettings


# For more information about settings standard check
# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    PROJECT_DIR: Path = Path(__file__).parent.parent.parent

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200",
    # "http://localhost:3000", "http://localhost:8080",
    # "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List = ["*"]

    # Environment configuration
    ENVIRONMENT: str = "development"

    # API Key configuration
    LOCAL_API_KEY: str = "default_api_key"

    # BigQuery configuration
    GOOGLE_CLOUD_PROJECT: str = "celestial-gecko-449316-d2"
    BIGQUERY_DATASET: str = "template_dataset"
    BIGQUERY_LOCATION: str = "US"
    PROJECT_ID: str = "celestial-gecko-449316-d2"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load Google Cloud credentials from key.json only in local environment
        if self.ENVIRONMENT.lower() == "local":
            key_path = self.PROJECT_DIR / "key.json"
            if key_path.exists():
                with open(key_path, "r") as key_file:
                    key_data = json.load(key_file)
                self.GOOGLE_CLOUD_PROJECT = key_data.get(
                    "project_id", self.GOOGLE_CLOUD_PROJECT
                )
                self.PROJECT_ID = key_data.get("project_id", self.PROJECT_ID)

    class Config:
        PROJECT_NAME: str = "Template Microservice"
        env_file = ".env"
        extra = "ignore"


settings = Settings()


# Google Cloud Credentials Helper
def get_google_credentials():
    """Get Google Cloud credentials based on environment"""
    if settings.ENVIRONMENT.lower() == "local":
        key_path = settings.PROJECT_DIR / "key.json"
        if key_path.exists():
            return service_account.Credentials.from_service_account_file(str(key_path))
        else:
            raise FileNotFoundError("key.json not found for local environment")
    else:
        # In production, use Application Default Credentials (ADC)
        # This will automatically use the service account attached to the GCP resource
        return None  # None means use default credentials


# BigQuery Client Settings
def get_bigquery_client() -> bigquery.Client:
    """Create BigQuery client with proper authentication"""
    credentials = get_google_credentials()

    if credentials:
        client = bigquery.Client(
            project=settings.GOOGLE_CLOUD_PROJECT,
            credentials=credentials,
            location=settings.BIGQUERY_LOCATION,
        )
    else:
        # Use default credentials (ADC) in production/cloud environments
        client = bigquery.Client(
            project=settings.GOOGLE_CLOUD_PROJECT, location=settings.BIGQUERY_LOCATION
        )

    return client


# Global variable for BigQuery client (lazy initialization)
_bigquery_client = None


def get_bigquery_client_instance():
    """Get or create BigQuery client instance (lazy initialization)"""
    global _bigquery_client
    if _bigquery_client is None:
        _bigquery_client = get_bigquery_client()
    return _bigquery_client


# Helper function to create dataset if it doesn't exist
def ensure_dataset_exists():
    """Create the dataset if it doesn't exist"""
    try:
        client = get_bigquery_client_instance()
        dataset_id = f"{settings.GOOGLE_CLOUD_PROJECT}.{settings.BIGQUERY_DATASET}"

        try:
            client.get_dataset(dataset_id)
        except Exception:
            # Dataset doesn't exist, create it
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = settings.BIGQUERY_LOCATION
            dataset.description = "Template microservice dataset"

            client.create_dataset(dataset, timeout=30)
            print(f"Created dataset {dataset_id}")
    except Exception as e:
        print(f"Warning: Could not initialize BigQuery: {e}")
        # Don't fail startup if BigQuery is not available
