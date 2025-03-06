#!/bin/bash

# API Parameter Analysis Workflow
# This script runs the complete workflow for API parameter analysis

echo "=== API Parameter Analysis Workflow ==="
echo ""

# Step 1: Collect data
echo "Step 1: Collecting data from APIs..."
echo "Running SODA data collection..."
python soda.py
echo "Running ArcGIS data collection..."
python arcgis.py
echo "Data collection complete."
echo ""

# Step 2: Extract metadata
echo "Step 2: Extracting metadata from API data..."
python extract_api_parameters.py
echo "Metadata extraction complete."
echo ""

# Step 3: Analyze and visualize
echo "Step 3: Analyzing metadata and generating visualizations..."
python analyze_apis.py
echo "Analysis complete."
echo ""

echo "=== Workflow Complete ==="
echo "Results are available in the 'output' folder."
echo "- SODA API results: output/soda/"
echo "- ArcGIS API results: output/arcgis/" 