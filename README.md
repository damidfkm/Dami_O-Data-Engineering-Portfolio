# py_gcs_bq

## The PROJECT

`py_gcs_bq` is a Python project designed to interact with Google Cloud Storage (GCS) and Google BigQuery. It allows users to:
1. Load flat files in CSV format from their local machine directly into a BigQuery table.
2. Load data from an API into a GCS bucket as JSON/JSONL and then into a BigQuery table.

The project ensures idempotency, meaning it handles duplicate records effectively, and is designed with reusability and ease of use in mind.

## Prerequisites

1. **Google Cloud SDK**: Ensure you have the Google Cloud SDK installed. You can download it from [here](https://cloud.google.com/sdk/docs/install).

2. **Python**: Make sure you have Python 3.7+ installed.

3. **Google Cloud Project**: You need access to a Google Cloud Project with the necessary APIs enabled:
    - Google Cloud Storage JSON API
    - BigQuery API

## Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.

### Step 2: Create a Service Account and Set Permissions

1. **Create Service Account**:
    ```sh
    gcloud iam service-accounts create your-service-account --display-name "Your Service Account"
    ```

2. **Grant Permissions**:
    ```sh
    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:your-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/bigquery.dataEditor"

    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:your-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/bigquery.jobUser"

    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:your-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/storage.admin"
    ```

3. **Generate JSON Key**:
    ```sh
    gcloud iam service-accounts keys create ./key.json --iam-account your-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
    ```

### Step 3: Clone the Repository

```sh
git clone https://github.com/your-username/py_gcs_bq.git
cd py_gcs_bq
```
### Step 4: Set Up a Virtual Environment and Install Dependencies
Create a Virtual Environment:

```sh
python -m venv venv
Activate the Virtual Environment:
```
On Windows:

```sh
venv\Scripts\activate
```

On macOS/Linux:
```sh
source venv/bin/activate
Install Dependencies:
```
```sh
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Create a .env File:
```
GCP_PROJECT_ID=
GCP_SERVICE_ACCOUNT_JSON=
API_URL=
GCS_BUCKET_NAME=
BIGQUERY_DATASET=
```
Update .env.example: Ensure the template file .env.example exists with the same keys but without the actual values.

### Step 6: Prepare Your Data
Place your CSV file in the py_gcs_bq/data/ directory.
```sh
py_gcs_bq/data/yourfile.csv
```
### Step 7: Run the Script
```sh
python main.py
```

### Project Structure
```
py_gcs_bq/
│
├── data/
│   └── yourfile.csv
│
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
└── key.json
```
### Explanation of Files
```sh
main.py: Main script containing all the functions and logic to interact with GCS and BigQuery.
config.py: Configuration file to manage environment variables.
requirements.txt: List of dependencies for the project.
.env.example: Example environment variables file to guide users in setting up their .env file.
key.json: Service account key file for Google Cloud authentication (not included in the repository for security reasons).
```
### Functions Explained
```sh
create_bucket_if_not_exists(bucket_name: str)
Creates a GCS bucket if it doesn't already exist.

create_dataset_if_not_exists(dataset_id: str)
Creates a BigQuery dataset if it doesn't already exist.

load_csv_to_bigquery(csv_file_path: str, table_id: str)
Loads a CSV file into a BigQuery table, truncating the table if it already exists.

fetch_data_from_api(api_url: str)
Fetches data from an API.

save_json_to_gcs(data: dict, bucket_name: str, destination_blob_name: str)
Saves JSON data to a GCS bucket.

convert_json_to_jsonlines(json_data: dict, jsonlines_path: str)
Converts JSON data to JSONLines format and saves it to a file.

load_jsonlines_to_bigquery(jsonlines_path: str, table_id: str)
Loads a JSONLines file into a BigQuery table, truncating the table if it already exists.

### Idempotency
The script ensures idempotency by:

Using WRITE_TRUNCATE as the write_disposition when loading data into BigQuery tables, which overwrites the existing table with new data.
Checking for the existence of GCS buckets and BigQuery datasets/tables before creating them, avoiding unnecessary re-creation.
```

### Common Errors and Solutions
403 Forbidden Error:
Ensure that the service account has the necessary permissions.
Verify that the roles BigQuery Data Editor, BigQuery Job User, and Storage Admin are assigned to the service account.

File Not Found:
Ensure that the key.json file is correctly placed in the project directory and the path in .env is correct.

Dependency Issues:
Ensure all dependencies are installed by running ```pip install -r requirements.txt.```
