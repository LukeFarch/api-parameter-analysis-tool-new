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
- Total SODA metadata files analyzed: 676
- Total parameters found: 29,477
- Unique parameter names: 6,161
- Average parameters per API: 43.6
- Most common parameter: "the_geom" (found in 266 APIs)
- Geographic data presence: 39.3% of APIs include geographic parameters

#### Top 50 SODA Parameters
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
| 21 | pop25plus | 83 | 0.28% |
| 22 | nohsdipl | 83 | 0.28% |
| 23 | hsgrad_sc | 83 | 0.28% |
| 24 | bachl_hghr | 83 | 0.28% |
| 25 | med_hh_inc | 83 | 0.28% |
| 26 | med_fam_in | 83 | 0.28% |
| 27 | per_cap_in | 83 | 0.28% |
| 28 | med_c_rent | 83 | 0.28% |
| 29 | med_g_rent | 83 | 0.28% |
| 30 | rnt_occ_hu | 83 | 0.28% |
| 31 | rntl400 | 83 | 0.28% |
| 32 | r800t999 | 83 | 0.28% |
| 33 | r1000t1249 | 83 | 0.28% |
| 34 | r1250t1499 | 83 | 0.28% |
| 35 | r1500t1999 | 83 | 0.28% |
| 36 | r2000pl | 83 | 0.28% |
| 37 | rnocshr | 83 | 0.28% |
| 38 | citz_birth | 83 | 0.28% |
| 39 | citz_nat | 83 | 0.28% |
| 40 | not_citz | 83 | 0.28% |
| 41 | born_in_co | 83 | 0.28% |
| 42 | brn_oth_st | 83 | 0.28% |
| 43 | ntv_b_o_us | 83 | 0.28% |
| 44 | foreign_b | 83 | 0.28% |
| 45 | pop_1p | 83 | 0.28% |
| 46 | same_house | 83 | 0.28% |
| 47 | same_cnty | 83 | 0.28% |
| 48 | same_state | 83 | 0.28% |
| 49 | diff_state | 83 | 0.28% |
| 50 | frm_abroad | 83 | 0.28% |

### ArcGIS API Analysis

#### Overview
- Total ArcGIS metadata files analyzed: 151
- Total parameters found: 7,367
- Unique parameter names: 2,851
- Average parameters per API: 48.8
- Most common parameter: "Shape__Length" (found in 511 APIs)
- Geographic data presence: 98.7% of APIs include shape parameters

#### Top 50 ArcGIS Parameters
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
| 21 | GlobalID | 21 | 0.29% |
| 22 | POPULATION | 19 | 0.26% |
| 23 | Species | 19 | 0.26% |
| 24 | SQMI | 18 | 0.24% |
| 25 | TAG_VALUE | 18 | 0.24% |
| 26 | OWNER | 17 | 0.23% |
| 27 | AcresGISCa | 14 | 0.19% |
| 28 | SqMilesGIS | 14 | 0.19% |
| 29 | POP_SQMI | 14 | 0.19% |
| 30 | tile | 14 | 0.19% |
| 31 | path | 14 | 0.19% |
| 32 | STATE_ABBR | 13 | 0.18% |
| 33 | STATE_FIPS | 13 | 0.18% |
| 34 | FIPS | 13 | 0.18% |
| 35 | info_ | 13 | 0.18% |
| 36 | GEOID | 12 | 0.16% |
| 37 | url | 12 | 0.16% |
| 38 | lastupdate | 11 | 0.15% |
| 39 | SHAPE__Area | 11 | 0.15% |
| 40 | SHAPE__Length | 11 | 0.15% |
| 41 | FUNCSTAT | 10 | 0.14% |
| 42 | STATE_NAME | 10 | 0.14% |
| 43 | COUNTY_FIPS | 10 | 0.14% |
| 44 | lgid | 10 | 0.14% |
| 45 | lgname | 10 | 0.14% |
| 46 | lgtypeid | 10 | 0.14% |
| 47 | lgstatusid | 10 | 0.14% |
| 48 | source | 10 | 0.14% |
| 49 | mail_address | 10 | 0.14% |
| 50 | alt_address | 10 | 0.14% |

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