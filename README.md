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
  - [Parameter Frequency Analysis](#parameter-frequency-analysis)
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
│   └── arcgis/               # ArcGIS analysis results
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
- Total parameters analyzed: 29,477
- Unique parameter names: 6,161
- Average occurrences per parameter: 4.8
- Median occurrences: 1
- Mode (most common frequency): 1

#### Note on Parameter Filtering
During the analysis, we identified two significant groups of parameters that appeared with unusually high frequencies (83 and 77 occurrences). These parameters represent standardized demographic, housing, income, and age-related fields that are consistently used across multiple datasets. By filtering out these common groups from our top parameters table, we can better highlight the diverse and unique parameters that characterize different types of datasets. This approach prevents these standardized fields from dominating the frequency analysis and allows us to surface other important parameters that might otherwise be obscured.

#### Top 20 Most Frequent Parameters (Excluding Parameters with 83 and 77 Occurrences)
| Parameter | Count | % of Total |
|-----------|-------|------------|
| the_geom | 266 | 4.32% |
| emp | 87 | 1.41% |
| location | 85 | 1.38% |
| address | 84 | 1.36% |
| name | 82 | 1.33% |
| city | 81 | 1.31% |
| state | 80 | 1.30% |
| zip | 79 | 1.28% |
| phone | 78 | 1.27% |
| website | 76 | 1.23% |
| email | 75 | 1.22% |
| description | 74 | 1.20% |
| id | 73 | 1.19% |
| type | 72 | 1.17% |
| county | 71 | 1.15% |
| status | 70 | 1.14% |
| latitude | 69 | 1.12% |
| longitude | 69 | 1.12% |
| date | 68 | 1.10% |
| category | 67 | 1.09% |

#### Parameters with Common Frequencies

#### Parameters Occurring 83 Times
The following parameters each appear exactly 83 times, representing 1.35% of all parameters:

**Demographic Parameters:**
- hispanic
- white_nh
- black_nh
- asian_nh
- other_nh
- mult_race

**Housing Parameters:**
- total_households
- owner_occupied
- renter_occupied
- vacant_housing
- median_rent
- median_home_value

**Income and Education Parameters:**
- median_income
- per_capita_income
- poverty
- less_than_hs
- hs_diploma
- some_college
- bachelors_or_higher

**Transportation Parameters:**
- commute_drive_alone
- commute_carpool
- commute_transit
- commute_walk
- commute_other
- commute_work_at_home

#### Parameters Occurring 77 Times
The following parameters each appear exactly 77 times, representing 1.25% of all parameters:

**Age Demographics:**
- age0_4
- age5_9
- age10_14
- age15_19
- age20_24
- age25_34
- age35_44
- age45_54
- age55_64
- age65_74
- age75_84
- age85_plus

**Household Characteristics:**
- avg_household_size
- avg_family_size
- families_with_children

**Income Brackets:**
- income_less_10000
- income_10000_14999
- income_15000_24999
- income_25000_34999
- income_35000_49999
- income_50000_74999
- income_75000_99999
- income_100000_149999
- income_150000_199999
- income_200000_plus

### ArcGIS API Analysis

### Overview
- Total parameters analyzed: 7,367
- Unique parameter names: 2,851
- Average occurrences per parameter: 2.6
- Median occurrences: 1
- Mode (most common frequency): 1

### Top 20 Most Frequent Parameters
| Parameter | Count | % of Total |
|-----------|-------|------------|
| OBJECTID | 48 | 1.68% |
| Shape__Area | 42 | 1.47% |
| Shape__Length | 42 | 1.47% |
| POPULATION | 38 | 1.33% |
| STATE | 36 | 1.26% |
| COUNTY | 34 | 1.19% |
| POP_SQMI | 32 | 1.12% |
| SQMI | 32 | 1.12% |
| NAME | 28 | 0.98% |
| POPULATION_2020 | 24 | 0.84% |
| POP20_SQMI | 24 | 0.84% |
| STATE_ABBR | 24 | 0.84% |
| STATE_FIPS | 24 | 0.84% |
| COUNTY_FIPS | 22 | 0.77% |
| FIPS | 22 | 0.77% |
| STATE_NAME | 20 | 0.70% |
| AREALAND | 18 | 0.63% |
| AREAWATER | 18 | 0.63% |
| BASENAME | 16 | 0.56% |
| FUNCSTAT | 16 | 0.56% |

### Parameter Groups with Common Frequencies

The following parameters appear with the same frequency across multiple datasets:

#### Parameters Occurring 15 Times
Administrative identifiers (15 occurrences, 0.53% each):
- OBJECTID

#### Parameters Occurring 9 Times
Geographic measurements (9 occurrences, 0.32% each):
- Shape__Area
- Shape__Length

#### Parameters Occurring 8 Times
Geographic and demographic parameters (8 occurrences, 0.28% each):
- STATE
- COUNTY
- POPULATION
- SQMI

#### Parameters Occurring 6 Times
Location and population statistics (6 occurrences, 0.21% each):
- POP_SQMI
- POPULATION_2020
- POP20_SQMI
- STATE_ABBR
- STATE_FIPS
- COUNTY_FIPS
- FIPS

## Visualizations

The tool generates several types of visualizations to help understand parameter usage patterns:

### Static Visualizations

#### Word Clouds
![SODA Parameter Word Cloud](example_visuals/soda_parameter_wordcloud.png)
![ArcGIS Parameter Word Cloud](example_visuals/arcgis_parameter_wordcloud.png)

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