import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GCP_SERVICE_ACCOUNT_JSON = os.getenv('GCP_SERVICE_ACCOUNT_JSON')
API_URL = os.getenv('API_URL')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET')

