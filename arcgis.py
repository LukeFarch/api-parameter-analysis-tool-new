"""
AWS Lambda script to parse a CSV file from ArcGIS and save the data locally.
"""

import json
import logging
import os
import csv
import pandas as pd
import sys

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO), 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

# Function to save data locally
def save_data_locally(df):
    print("Starting save_data_locally function")
    # Create ArcGis directory if it doesn't exist
    api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ArcGis")
    print(f"API directory path: {api_dir}")
    if not os.path.exists(api_dir):
        print(f"Creating directory: {api_dir}")
        os.makedirs(api_dir)
        logger.info(f"Created directory: {api_dir}")
    else:
        print(f"Directory already exists: {api_dir}")
    
    # Save the full dataframe as CSV
    csv_path = os.path.join(api_dir, "all_apis.csv")
    print(f"Saving CSV to: {csv_path}")
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved all APIs to {csv_path}")
    
    # Save each API as a separate JSON file
    total_rows = len(df)
    print(f"Total APIs to save: {total_rows}")
    logger.info(f"Total APIs to save: {total_rows}")
    
    for index, row in df.iterrows():
        try:
            print(f"Processing API {index + 1}/{total_rows}: {row['name']}")
            logger.info(f"Processing API {index + 1}/{total_rows}: {row['name']}")
            
            # Create a clean filename from the API name
            filename = row['name'].lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = ''.join(c for c in filename if c.isalnum() or c == '_')
            filename = f"{filename}.json"
            
            # Convert categories to a list
            categories = [c.strip() for c in row['category'].split(',')] if pd.notna(row['category']) else []
            
            # Create a dictionary with the API data
            api_data = {
                'name': row['name'],
                'description': row['description'],
                'categories': categories,
                'url': row['url'],
                'organization': row['organization'],
                'org_name': row['org_name']
            }
            
            # Save the API data as a JSON file
            json_path = os.path.join(api_dir, filename)
            print(f"Saving API to: {json_path}")
            with open(json_path, 'w') as f:
                json.dump(api_data, f, indent=2)
                
            logger.info(f"Saved API to {json_path}")
            
        except Exception as row_error:
            print(f"Error processing API {index + 1}: {row_error}")
            logger.error(f"Error processing API {index + 1}: {row_error}")

    print("Data processing completed.")
    logger.info("Data processing completed.")

# Main Lambda handler
def lambda_handler(event, context):
    print("Starting lambda_handler function")
    file_url = "https://hub.arcgis.com/api/feed/all/csv?target=geodata.colorado.gov"

    try:
        print(f"Downloading and processing file from {file_url}")
        logger.info(f"Downloading and processing file from {file_url}")
        df = pd.read_csv(file_url)
        print(f"Downloaded CSV with {len(df)} rows")
        df = df.rename(columns={
            'title': 'name',
            'tags': 'category',
            'source': 'organization',
            'owner': 'org_name'
        })
        required_columns = ['name', 'description', 'category', 'url', 'organization', 'org_name']
        print(f"Checking for required columns: {required_columns}")
        print(f"Available columns: {df.columns.tolist()}")
        if not all(col in df.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            print(f"Missing required columns: {', '.join(missing_columns)}")
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        save_data_locally(df)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File processed successfully. APIs saved locally."})
        }
    except Exception as e:
        print(f"Error processing file: {e}")
        logger.error(f"Error processing file: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error processing file: {e}"})
        }

# Add this to make the script runnable directly
if __name__ == "__main__":
    print("Script started")
    lambda_handler(None, None)
    print("Script finished") 