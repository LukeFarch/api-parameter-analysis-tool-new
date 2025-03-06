#!/usr/bin/env python3
"""
API Parameter Extractor

This script extracts API parameters from both Soda and ArcGIS APIs by:
1. Scanning JSON files in the Soda and ArcGis folders
2. Extracting base URLs from each file
3. Fetching metadata from the respective APIs
4. Saving the metadata to MetaDataSoda and MetaDataArcgis folders

Usage:
    python extract_api_parameters.py
"""

import os
import json
import time
import requests
import pandas as pd
from collections import Counter
from urllib.parse import urlparse, parse_qs
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Constants
SODA_FOLDER = 'Soda'
ARCGIS_FOLDER = 'ArcGis'
METADATA_SODA_FOLDER = 'MetaDataSoda'
METADATA_ARCGIS_FOLDER = 'MetaDataArcgis'
MAX_WORKERS = 10  # Number of concurrent requests
REQUEST_DELAY = 0.1  # Delay between requests to avoid rate limiting

def extract_dataset_id_from_url(url):
    """Extract the dataset ID from a SODA API URL."""
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Extract the path
        path = parsed_url.path
        
        # The dataset ID is typically the last part of the path before .json
        match = re.search(r'/([^/]+)\.json$', path)
        if match:
            return match.group(1)
        
        # If not found with the pattern above, try another approach
        parts = path.split('/')
        if parts:
            last_part = parts[-1]
            if '.' in last_part:
                return last_part.split('.')[0]
        
        return None
    except Exception as e:
        print(f"Error extracting dataset ID from {url}: {e}")
        return None

def get_soda_metadata(dataset_id, domain):
    """Fetch metadata for a SODA API dataset."""
    try:
        # Construct the metadata URL
        metadata_url = f"https://{domain}/api/views/metadata/v1/{dataset_id}"
        
        # Fetch the metadata
        response = requests.get(metadata_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch metadata for {dataset_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching metadata for {dataset_id}: {e}")
        return None

def get_soda_columns(dataset_id, domain):
    """Fetch column information for a SODA API dataset."""
    try:
        # Construct the columns URL
        columns_url = f"https://{domain}/api/views/{dataset_id}/columns"
        
        # Fetch the columns
        response = requests.get(columns_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch columns for {dataset_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching columns for {dataset_id}: {e}")
        return None

def get_arcgis_metadata(service_url):
    """Fetch metadata for an ArcGIS REST service."""
    try:
        # Construct the metadata URL
        metadata_url = f"{service_url}?f=json"
        
        # Fetch the metadata
        response = requests.get(metadata_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch metadata for {service_url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching metadata for {service_url}: {e}")
        return None

def get_arcgis_layer_info(service_url, layer_id):
    """Fetch layer information for an ArcGIS REST service layer."""
    try:
        # Construct the layer URL
        layer_url = f"{service_url}/{layer_id}?f=json"
        
        # Fetch the layer information
        response = requests.get(layer_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch layer info for {layer_url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching layer info for {layer_url}: {e}")
        return None

def process_soda_file(file_path):
    """Process a SODA JSON file to extract API parameters."""
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the base URL
        base_url = data.get('base_url')
        if not base_url:
            print(f"No base_url found in {file_path}")
            return None
        
        # Extract the dataset ID and domain
        dataset_id = extract_dataset_id_from_url(base_url)
        parsed_url = urlparse(base_url)
        domain = parsed_url.netloc
        
        if not dataset_id or not domain:
            print(f"Could not extract dataset ID or domain from {base_url}")
            return None
        
        # Get metadata and columns
        metadata = get_soda_metadata(dataset_id, domain)
        columns = get_soda_columns(dataset_id, domain)
        
        # Create a result object
        result = {
            'file_path': file_path,
            'base_url': base_url,
            'dataset_id': dataset_id,
            'domain': domain,
            'metadata': metadata,
            'columns': columns
        }
        
        # Extract parameters (column names and types)
        parameters = []
        if columns:
            for column in columns:
                param = {
                    'name': column.get('name', ''),
                    'field_name': column.get('fieldName', ''),
                    'type': column.get('dataTypeName', ''),
                    'description': column.get('description', '')
                }
                parameters.append(param)
        
        result['parameters'] = parameters
        
        # Save the result to the metadata folder
        output_file = os.path.join(METADATA_SODA_FOLDER, f"{dataset_id}_metadata.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        return result
    except Exception as e:
        print(f"Error processing SODA file {file_path}: {e}")
        return None

def process_arcgis_file(file_path):
    """Process an ArcGIS JSON file to extract API parameters."""
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the service URL
        service_url = data.get('url')
        if not service_url:
            print(f"No url found in {file_path}")
            return None
        
        # Check if it's an ArcGIS REST service URL
        if 'arcgis/rest/services' not in service_url:
            print(f"Not an ArcGIS REST service URL: {service_url}")
            return None
        
        # Get service metadata
        metadata = get_arcgis_metadata(service_url)
        if not metadata:
            return None
        
        # Create a result object
        result = {
            'file_path': file_path,
            'service_url': service_url,
            'metadata': metadata,
            'layers': []
        }
        
        # Extract parameters from layers
        parameters = []
        
        # Check if the service has layers
        layers = metadata.get('layers', [])
        if layers:
            for layer in layers:
                layer_id = layer.get('id')
                if layer_id is not None:
                    # Get layer information
                    layer_info = get_arcgis_layer_info(service_url, layer_id)
                    if layer_info:
                        result['layers'].append(layer_info)
                        
                        # Extract fields as parameters
                        fields = layer_info.get('fields', [])
                        for field in fields:
                            param = {
                                'name': field.get('name', ''),
                                'alias': field.get('alias', ''),
                                'type': field.get('type', ''),
                                'description': ''
                            }
                            parameters.append(param)
        
        result['parameters'] = parameters
        
        # Generate a unique identifier for the service
        service_name = os.path.basename(file_path).replace('.json', '')
        
        # Save the result to the metadata folder
        output_file = os.path.join(METADATA_ARCGIS_FOLDER, f"{service_name}_metadata.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        return result
    except Exception as e:
        print(f"Error processing ArcGIS file {file_path}: {e}")
        return None

def process_files_with_progress(files, process_func):
    """Process files with progress bar and threading."""
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_file = {executor.submit(process_func, file_path): file_path for file_path in files}
        
        # Process as they complete with a progress bar
        for future in tqdm(future_to_file, desc="Processing files"):
            file_path = future_to_file[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                # Add a small delay to avoid rate limiting
                time.sleep(REQUEST_DELAY)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    return results

def main():
    """Main function to run the API parameter extraction."""
    print("Starting API parameter extraction...")
    
    # Ensure metadata folders exist
    os.makedirs(METADATA_SODA_FOLDER, exist_ok=True)
    os.makedirs(METADATA_ARCGIS_FOLDER, exist_ok=True)
    
    # Get all JSON files in the SODA folder
    soda_files = []
    if os.path.exists(SODA_FOLDER):
        for file in os.listdir(SODA_FOLDER):
            if file.endswith('.json'):
                soda_files.append(os.path.join(SODA_FOLDER, file))
    
    # Get all JSON files in the ArcGIS folder
    arcgis_files = []
    if os.path.exists(ARCGIS_FOLDER):
        for file in os.listdir(ARCGIS_FOLDER):
            if file.endswith('.json'):
                arcgis_files.append(os.path.join(ARCGIS_FOLDER, file))
    
    print(f"Found {len(soda_files)} SODA files and {len(arcgis_files)} ArcGIS files")
    
    # Process SODA files
    print("\nProcessing SODA files...")
    soda_results = process_files_with_progress(soda_files, process_soda_file)
    
    # Process ArcGIS files
    print("\nProcessing ArcGIS files...")
    arcgis_results = process_files_with_progress(arcgis_files, process_arcgis_file)
    
    # Print summary
    print("\n===== API PARAMETER EXTRACTION SUMMARY =====")
    print(f"SODA files processed: {len(soda_files)}")
    print(f"SODA metadata files created: {len(soda_results)}")
    print(f"ArcGIS files processed: {len(arcgis_files)}")
    print(f"ArcGIS metadata files created: {len(arcgis_results)}")
    
    print("\nMetadata saved to:")
    print(f"- {METADATA_SODA_FOLDER}/")
    print(f"- {METADATA_ARCGIS_FOLDER}/")
    
    print("\nExtraction complete! You can now run analyze_apis.py to analyze the extracted metadata.")

if __name__ == "__main__":
    main() 