"""
AWS Lambda script to process JSON data from the Colorado Open Data API and save it locally.
"""

import json
import logging
import os
import requests
import pandas as pd
import re
import time
from pathlib import Path

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO),
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Helper function to construct endpoint URL
def construct_endpoint(identifier):
    base_url = "https://data.colorado.gov/resource/"
    return f"{base_url}{identifier}.json"

# Function to save data locally
def save_data_locally(df):
    try:
        # Create Soda directory if it doesn't exist
        soda_dir = Path("Soda")
        soda_dir.mkdir(exist_ok=True)
        
        # Save the full DataFrame as CSV
        csv_path = soda_dir / "all_soda_apis.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved full dataset to {csv_path}")
        
        # Save each API as a separate JSON file
        total_apis = len(df)
        logger.info(f"Processing {total_apis} APIs")
        
        for index, row in df.iterrows():
            try:
                # Create a safe filename from the API name
                api_name = row['name']
                safe_filename = re.sub(r'[^\w\s-]', '', api_name.lower())
                safe_filename = re.sub(r'[\s-]+', '_', safe_filename)
                
                # Save the API data as JSON
                json_path = soda_dir / f"{safe_filename}.json"
                print(f"Processing API {index+1}/{total_apis}: {api_name}")
                logger.info(f"Processing API {index+1}/{total_apis}: {api_name}")
                
                print(f"Saving API to: {json_path}")
                with open(json_path, 'w') as f:
                    json.dump(row.to_dict(), f, indent=2)
                logger.info(f"Saved API to {json_path}")
                
            except Exception as e:
                print(f"Error saving API {row.get('name', 'unknown')}: {e}")
                logger.error(f"Error saving API {row.get('name', 'unknown')}: {e}")
        
        logger.info(f"Data processing completed. Saved {total_apis} APIs to {soda_dir}")
        print(f"Data processing completed.")
        
    except Exception as e:
        print(f"Error saving data locally: {e}")
        logger.error(f"Error saving data locally: {e}")
        raise

# Main Lambda handler
def lambda_handler(event, context):
    api_url = "https://data.colorado.gov/api/views/"

    try:
        logger.info(f"Downloading and processing data from {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Filter items with provenance = "official"
        official_items = [
            {
                "name": item.get('name', ''),
                "description": item.get('description', ''),
                "category": item.get('tags', []),
                "base_url": construct_endpoint(item.get('modifyingViewUid', item['id'])),
                "organization": item.get('attribution', {}).get('name', ''),
                "organization_contact": item.get('owner', {}).get('displayName', '')
            }
            for item in data if item.get('provenance') == 'official' and item.get('assetType') == 'dataset'
        ]

        df = pd.DataFrame(official_items)
        required_columns = ['name', 'description', 'category', 'base_url', 'organization', 'organization_contact']
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
        print(f"Error processing data: {e}")
        logger.error(f"Error processing data: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error processing data: {e}"})
        }

# Add this to make the script runnable directly
if __name__ == "__main__":
    print("Script started")
    lambda_handler(None, None)
    print("Script finished")