# API Parameter Analysis Tool

A comprehensive tool for analyzing parameters from SODA and ArcGIS APIs, extracting metadata, and generating insightful visualizations to understand parameter usage patterns.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Analysis Results](#analysis-results)
  - [SODA API Analysis](#soda-api-analysis)
  - [ArcGIS API Analysis](#arcgis-api-analysis)
- [Visualizations](#visualizations)

## Overview

The API Parameter Analysis Tool is designed to help developers and analysts understand the parameter patterns across SODA and ArcGIS APIs. It extracts metadata, analyzes parameter usage, and generates both static and interactive visualizations.

## Features

- **Automated Data Collection**: Scripts to collect data from both SODA and ArcGIS APIs
- **Metadata Extraction**: Comprehensive metadata extraction from API responses
- **Parameter Analysis**: Deep analysis of parameter usage patterns
- **Visualization Generation**: Both static and interactive visualizations
- **Detailed Reporting**: Comprehensive reports on parameter usage

## Prerequisites

- Python 3.6+
- Required Python packages:
  ```
  requests>=2.25.1
  pandas>=1.2.4
  matplotlib>=3.4.2
  seaborn>=0.11.1
  wordcloud>=1.8.1
  numpy>=1.20.3
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/api-parameter-analysis-tool.git
   cd api-parameter-analysis-tool
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the complete workflow:
   ```bash
   ./run_workflow.sh
   ```

2. Or run individual scripts:
   ```bash
   # Collect data
   python soda.py
   python arcgis.py
   
   # Extract metadata
   python extract_api_parameters.py
   
   # Analyze and visualize
   python analyze_apis.py
   ```

## Project Structure

```
.
├── Soda/                      # Raw SODA API data
├── ArcGis/                    # Raw ArcGIS API data
├── MetaDataSoda/              # Extracted SODA metadata
├── MetaDataArcGis/            # Extracted ArcGIS metadata
├── output/                    # Analysis output
│   ├── soda/                  # SODA analysis results
│   └── arcgis/                # ArcGIS analysis results
├── scripts/
│   ├── soda.py               # SODA data collection
│   ├── arcgis.py             # ArcGIS data collection
│   ├── extract_api_parameters.py  # Metadata extraction
│   └── analyze_apis.py       # Analysis and visualization
└── README.md                 # This file
```

## Analysis Results

### SODA API Analysis

#### Overview
- Total SODA metadata files analyzed: 676
- Total parameters found: 29,477
- Unique parameter names: 6,161

#### Top 20 SODA Parameters
| Rank | Parameter | Count | Percentage |
|------|-----------|-------|------------|
| 1 | the_geom | 266 | 0.90% |
| 2 | emp | 87 | 0.30% |
| 3 | hispanic | 83 | 0.28% |
| 4 | white_nh | 83 | 0.28% |
| 5 | black_nh | 83 | 0.28% |
| 6 | ntvam_nh | 83 | 0.28% |
| 7 | asian_nh | 83 | 0.28% |
| 8 | hawpi_nh | 83 | 0.28% |
| 9 | other_nh | 83 | 0.28% |
| 10 | twoplus_nh | 83 | 0.28% |
| 11 | male | 83 | 0.28% |
| 12 | female | 83 | 0.28% |
| 13 | ageless18 | 83 | 0.28% |
| 14 | age18_24 | 83 | 0.28% |
| 15 | med_age | 83 | 0.28% |
| 16 | housing_un | 83 | 0.28% |
| 17 | occ_hu | 83 | 0.28% |
| 18 | vac_hu | 83 | 0.28% |
| 19 | owned | 83 | 0.28% |
| 20 | rented | 83 | 0.28% |

### ArcGIS API Analysis

#### Overview
- Total ArcGIS metadata files analyzed: 151
- Total parameters found: 7,367
- Unique parameter names: 2,851

#### Top 20 ArcGIS Parameters
| Rank | Parameter | Count | Percentage |
|------|-----------|-------|------------|
| 1 | Shape__Length | 511 | 6.94% |
| 2 | Shape__Area | 469 | 6.37% |
| 3 | FID | 336 | 4.56% |
| 4 | INPUT_DATE | 333 | 4.52% |
| 5 | EDIT_DATE | 331 | 4.49% |
| 6 | ACTIVITYCO | 311 | 4.22% |
| 7 | OBJECTID | 247 | 3.35% |
| 8 | Name | 65 | 0.88% |
| 9 | Note | 61 | 0.83% |
| 10 | UpdateComm | 48 | 0.65% |
| 11 | BufferDist | 48 | 0.65% |
| 12 | Species_Ac | 48 | 0.65% |
| 13 | Activity_C | 47 | 0.64% |
| 14 | NAME | 41 | 0.56% |
| 15 | HU_12_NAME | 34 | 0.46% |
| 16 | COUNTY | 31 | 0.42% |
| 17 | STATE | 31 | 0.42% |
| 18 | COMMENTS | 29 | 0.39% |
| 19 | SOURCE | 25 | 0.34% |
| 20 | CITY | 23 | 0.31% |

## Visualizations

The tool generates several types of visualizations to help understand parameter usage patterns:

### Static Visualizations

#### Word Clouds
![SODA Parameter Word Cloud](example_visuals/soda_parameter_wordcloud.png)
![ArcGIS Parameter Word Cloud](example_visuals/arcgis_parameter_wordcloud.png)

#### Parameter Distribution
![SODA Parameter Distribution](example_visuals/soda_parameter_distribution.png)
![ArcGIS Parameter Distribution](example_visuals/arcgis_parameter_distribution.png)

#### Top Parameters
![SODA Top Parameters](example_visuals/soda_top_parameters.png)
![ArcGIS Top Parameters](example_visuals/arcgis_top_parameters.png)

#### Parameter Treemaps
![SODA Parameter Treemap](example_visuals/soda_parameter_treemap.png)
![ArcGIS Parameter Treemap](example_visuals/arcgis_parameter_treemap.png)

### Interactive Visualizations

The tool also generates interactive visualizations that can be found in the `output/interactive` directory after running the analysis:

- Interactive Bar Charts
- Interactive Treemaps
- Parameter Relationship Networks 