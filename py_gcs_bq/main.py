import json
import requests
from google.cloud import storage, bigquery
from google.oauth2 import service_account
from config import GCP_PROJECT_ID, GCP_SERVICE_ACCOUNT_JSON, API_URL, GCS_BUCKET_NAME, BIGQUERY_DATASET

# Set up Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_JSON)

def create_bucket_if_not_exists(bucket_name: str):
    """
    Create a GCS bucket if it doesn't already exist.
    
    Args:
    bucket_name (str): The name of the bucket to create.
    """
    client = storage.Client(credentials=credentials, project=GCP_PROJECT_ID)
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create(location='us')
        print(f"Bucket {bucket_name} created.")
    else:
        print(f"Bucket {bucket_name} already exists.")

def create_dataset_if_not_exists(dataset_id: str):
    """
    Create a BigQuery dataset if it doesn't already exist.
    
    Args:
    dataset_id (str): The ID of the dataset to create.
    """
    client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
    dataset = bigquery.Dataset(dataset_id)
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists.")
    except:
        client.create_dataset(dataset)
        print(f"Dataset {dataset_id} created.")

def load_csv_to_bigquery(csv_file_path: str, table_id: str):
    """
    Load a CSV file into a BigQuery table. If the table already exists, it will be overwritten.
    
    Args:
    csv_file_path (str): The path to the CSV file.
    table_id (str): The ID of the BigQuery table.
    """
    client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    with open(csv_file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()
    print(f"Loaded {csv_file_path} into {table_id}")

def fetch_data_from_api(api_url: str):
    """
    Fetch data from an API.
    
    Args:
    api_url (str): The URL of the API.
    
    Returns:
    dict: The JSON data fetched from the API.
    """
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def save_json_to_gcs(data: dict, bucket_name: str, destination_blob_name: str):
    """
    Save JSON data to a GCS bucket.
    
    Args:
    data (dict): The JSON data to save.
    bucket_name (str): The name of the GCS bucket.
    destination_blob_name (str): The destination path in the GCS bucket.
    """
    client = storage.Client(credentials=credentials, project=GCP_PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_string(json.dumps(data), content_type='application/json')
    print(f"Data saved to {bucket_name}/{destination_blob_name}")

def convert_json_to_jsonlines(json_data: dict, jsonlines_path: str):
    """
    Convert JSON data to JSONLines format and save to a file.
    
    Args:
    json_data (dict): The JSON data to convert.
    jsonlines_path (str): The path to save the JSONLines file.
    """
    with open(jsonlines_path, 'w') as f:
        for item in json_data:
            f.write(json.dumps(item) + '\n')

def load_jsonlines_to_bigquery(jsonlines_path: str, table_id: str):
    """
    Load a JSONLines file into a BigQuery table. If the table already exists, it will be overwritten.
    
    Args:
    jsonlines_path (str): The path to the JSONLines file.
    table_id (str): The ID of the BigQuery table.
    """
    client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    with open(jsonlines_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()
    print(f"Loaded data from {jsonlines_path} into {table_id}")

if __name__ == "__main__":
    # Step 1: Create bucket and dataset if they don't exist
    create_bucket_if_not_exists(GCS_BUCKET_NAME)
    create_dataset_if_not_exists(f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}")

    # Step 2: Load CSV into BigQuery
    load_csv_to_bigquery("py_gcs_bq/data/customers.csv", f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.your_table_name")

    # Step 3: Fetch data from API and save to GCS
    data = fetch_data_from_api(API_URL)
    save_json_to_gcs(data, GCS_BUCKET_NAME, 'data.json')

    # Step 4: Convert JSON to JSONLines and load into BigQuery
    jsonlines_path = 'py_gcs_bq/data/data.jsonl'
    convert_json_to_jsonlines(data, jsonlines_path)
    load_jsonlines_to_bigquery(jsonlines_path, f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.your_table_name")
