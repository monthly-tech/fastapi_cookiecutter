import json
import logging
from typing import Optional, Union
from google.api_core.client_options import ClientOptions
from google.cloud import secretmanager, storage
from google.oauth2 import service_account

# Import settings to get LOCAL_API_KEY
from core.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCloudServices:
    def __init__(self):
        try:
            self.project_id = settings.GCP_PROJECT_ID
            client_options = ClientOptions(quota_project_id=self.project_id)

            # Google Secret Manager initialization
            # if exists credentials file, use it
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                credentials = service_account.Credentials.from_service_account_file(
                    settings.GOOGLE_APPLICATION_CREDENTIALS,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"],
                )

                # Google Cloud Secret Manager initialization
                self.sm_client = secretmanager.SecretManagerServiceClient(
                    credentials=credentials, client_options=client_options
                )
                
                # Google Cloud Storage initialization
                self.storage_client = storage.Client(
                    credentials=credentials, project=self.project_id
                )
            else:
                # Use default credentials (ADC - Application Default Credentials)
                self.sm_client = secretmanager.SecretManagerServiceClient(
                    client_options=client_options
                )

                # Use default credentials (ADC - Application Default Credentials)
                self.storage_client = storage.Client(project=self.project_id)

            logger.info("Google Cloud Services initialized successfully")
            logger.info(f"Project ID: {self.project_id}")

        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud Services: {str(e)}")
            raise Exception(f"Could not initialize Google Cloud Services: {str(e)}")

    def get_monthly_secrets(self, version: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{settings.GCP_MONTHLY_PROVIDERS_SECRET_ID}/versions/{version}"
        response = self.sm_client.access_secret_version(request={"name": name})
        return json.loads(response.payload.data.decode("utf-8"))

    def upload_file_to_bucket(
        self, bucket_name: str, source_file_path: str, destination_blob_name: str
    ) -> tuple[bool, Optional[str]]:
        """
        Uploads a file to a Google Cloud Storage bucket

        Args:
            bucket_name (str): Name of the GCS bucket
            source_file_path (str): Path to the local file to upload
            destination_blob_name (str): Name for the file in the bucket

        Returns:
            tuple[bool, Optional[str]]: (success, error_message_or_public_url)
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            # Upload the file
            blob.upload_from_filename(source_file_path)

            logger.info(
                f"File {source_file_path} uploaded to {bucket_name}/{destination_blob_name}"
            )

            # Return the public URL of the uploaded file
            public_url = f"gs://{bucket_name}/{destination_blob_name}"
            return True, public_url

        except Exception as e:
            error_msg = f"Error uploading file to bucket: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def read_file_from_bucket(
        self, bucket_name: str, blob_name: str, as_text: bool = True
    ) -> tuple[bool, Union[str, bytes, None]]:
        """
        Reads a file from a Google Cloud Storage bucket

        Args:
            bucket_name (str): Name of the GCS bucket
            blob_name (str): Name of the file in the bucket
            as_text (bool): If True, returns content as string. If False, returns as bytes

        Returns:
            tuple[bool, Union[str, bytes, None]]: (success, file_content_or_error_message)
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Check if the blob exists
            if not blob.exists():
                error_msg = f"File {blob_name} not found in bucket {bucket_name}"
                logger.error(error_msg)
                return False, error_msg

            # Download the file content
            if as_text:
                content = blob.download_as_text()
            else:
                content = blob.download_as_bytes()

            logger.info(f"File {blob_name} successfully read from bucket {bucket_name}")

            return True, content

        except Exception as e:
            error_msg = f"Error reading file from bucket: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
