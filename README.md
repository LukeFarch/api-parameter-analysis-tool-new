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

#### Top Parameters Analysis
##### Frequency Table
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

##### Visualization
![Top 30 SODA Parameters (Excluding 83/77 Occurrences)](output/soda/visualizations/soda_top_parameters.png)

The bar chart above visualizes the top 30 most frequent parameters in the SODA API datasets, excluding parameters that occur exactly 83 or 77 times. This visualization helps highlight the diverse range of commonly used parameters across different datasets while filtering out the standardized demographic and socioeconomic parameters.

#### Parameter Groups Analysis

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

#### Overview
- Total parameters analyzed: 3,715
- Unique parameter names: 2,851
- Average occurrences per parameter: 1.3
- Median occurrences: 1
- Mode (most common frequency): 1

#### Top Parameters Analysis
##### Frequency Table
| Parameter | Count | % of Total |
|-----------|-------|------------|
| OBJECTID | 94 | 3.30% |
| Shape__Length | 63 | 2.21% |
| Shape__Area | 47 | 1.65% |
| NAME | 21 | 0.74% |
| STATE | 15 | 0.53% |
| GlobalID | 14 | 0.49% |
| url | 12 | 0.42% |
| FID | 11 | 0.39% |
| COUNTY | 11 | 0.39% |
| lastupdate | 11 | 0.39% |
| SHAPE__Area | 11 | 0.39% |
| SHAPE__Length | 11 | 0.39% |
| CITY | 9 | 0.32% |
| Direction | 9 | 0.32% |
| Longitude | 8 | 0.28% |
| Latitude | 8 | 0.28% |
| FIPS | 8 | 0.28% |
| City | 8 | 0.28% |
| Highway | 8 | 0.28% |
| EndRefPoint | 8 | 0.28% |

##### Visualization
![ArcGIS Top Parameters](output/arcgis/visualizations/arcgis_top_parameters.png)

The bar chart above shows the distribution of the most frequent parameters in the ArcGIS API datasets. Note that ArcGIS parameters tend to be more standardized across datasets, with geometric and identification parameters being the most common.

#### Parameter Groups Analysis

The following section shows groups of parameters that frequently appear together in the same datasets. An important note about the counts:

1. **Total Occurrences** (shown in the table above): This counts every time a parameter appears, including multiple occurrences within different layers of the same dataset.
2. **Dataset Co-occurrences** (shown below): This counts the number of unique datasets where these parameters appear together as a group.

For example, when a parameter appears "in 6 datasets", it means it's found in 6 different metadata files, but might appear multiple times within each file due to multiple data layers.

#### Parameters Co-occurring in 15 Datasets
Administrative identifiers:
- OBJECTID (found in 15 unique datasets, appearing 94 times total across all layers)

#### Parameters Co-occurring in 9 Datasets
Geographic measurements that appear together:
- Shape__Area (found in 9 unique datasets, appearing 47 times total across all layers)
- Shape__Length (found in 9 unique datasets, appearing 63 times total across all layers)

#### Parameters Co-occurring in 8 Datasets
Geographic and demographic parameters that appear as a group:
- STATE (found in 8 unique datasets, appearing 15 times total across all layers)
- COUNTY (found in 8 unique datasets, appearing 11 times total across all layers)
- POPULATION (found in 8 unique datasets, appearing 38 times total across all layers)
- SQMI (found in 8 unique datasets, appearing 32 times total across all layers)

#### Parameters Co-occurring in 6 Datasets
Location and population statistics that appear together:
- POP_SQMI (found in 6 unique datasets, appearing 32 times total across all layers)
- POPULATION_2020 (found in 6 unique datasets, appearing 24 times total across all layers)
- POP20_SQMI (found in 6 unique datasets, appearing 24 times total across all layers)
- STATE_ABBR (found in 6 unique datasets, appearing 24 times total across all layers)
- STATE_FIPS (found in 6 unique datasets, appearing 24 times total across all layers)
- COUNTY_FIPS (found in 6 unique datasets, appearing 22 times total across all layers)
- FIPS (found in 6 unique datasets, appearing 22 times total across all layers)

This grouping helps identify standardized parameter sets that are commonly used together in ArcGIS datasets. The higher total occurrence counts are due to these parameters appearing in multiple layers within each dataset, which is a common practice in GIS data where the same schema is applied to different geographic levels or views of the data.

## Additional Visualizations

### Word Clouds
These word clouds provide a visual representation of parameter frequency across all datasets:

#### SODA Parameters
![SODA Parameter Word Cloud](output/soda/visualizations/soda_parameter_wordcloud.png)

#### ArcGIS Parameters
![ArcGIS Parameter Word Cloud](output/arcgis/visualizations/arcgis_parameter_wordcloud.png)

### Parameter Distribution Treemaps
These treemaps show the hierarchical distribution of parameter frequencies:

#### SODA Parameters
![SODA Parameter Treemap](output/soda/visualizations/soda_parameter_treemap.png)

#### ArcGIS Parameters
![ArcGIS Parameter Treemap](output/arcgis/visualizations/arcgis_parameter_treemap.png)

### Interactive Visualizations

The tool also generates interactive versions of these visualizations that can be found in the following directories:

- SODA Interactive Visualizations: `output/soda/interactive/`
- ArcGIS Interactive Visualizations: `output/arcgis/interactive/`

These interactive visualizations include:
- Interactive Bar Charts
- Interactive Treemaps
- Parameter Relationship Networks

### Parameter Naming Patterns
These visualizations show the distribution of different naming conventions (camelCase, UPPERCASE, etc.) across parameters:

#### SODA Parameters
![SODA Parameter Patterns](output/soda/visualizations/soda_parameter_patterns.png)

The above visualization shows the distribution of data types in SODA parameters.

#### SODA Naming Conventions
![SODA Naming Conventions](output/soda/visualizations/soda_naming_conventions.png)

The above visualization shows the distribution of naming conventions (snake_case, camelCase, UPPERCASE, etc.) in SODA parameters.

#### ArcGIS Parameters
![ArcGIS Parameter Patterns](output/arcgis/visualizations/arcgis_parameter_patterns.png)

The above visualization shows the distribution of data types in ArcGIS parameters.

#### ArcGIS Naming Conventions
![ArcGIS Naming Conventions](output/arcgis/visualizations/arcgis_naming_conventions.png)

The above visualization shows the distribution of naming conventions (PascalCase, UPPERCASE, snake_case, etc.) in ArcGIS parameters.

## Appendix: Top 100 Parameters

### SODA Top 100 Parameters
*Note: Excludes parameters occurring exactly 83 or 77 times*

| Rank | Parameter | Count |
|------|-----------|-------|
| 1 | the_geom | 266 |
| 2 | emp | 87 |
| 3 | unemp | 78 |
| 4 | laborforce | 78 |
| 5 | OBJECTID | 73 |
| 6 | Counties | 70 |
| 7 | County | 69 |
| 8 | r400t599 | 65 |
| 9 | r600t799 | 65 |
| 10 | geonum | 61 |
| 11 | Year | 56 |
| 12 | geoname | 55 |
| 13 | civ_ni_p | 52 |
| 14 | NAME | 44 |
| 15 | year | 42 |
| 16 | WHITE_NH | 39 |
| 17 | ASIAN_NH | 39 |
| 18 | HISPANIC | 39 |
| 19 | AGE65PLUS | 39 |
| 20 | MALE | 39 |
| 21 | OTHER_NH | 39 |
| 22 | BLACK_NH | 39 |
| 23 | FEMALE | 39 |
| 24 | Shape_Leng | 37 |
| 25 | ROUTE | 37 |
| 26 | STATE | 35 |
| 27 | HOUSEHOLDS | 32 |
| 28 | MED_AGE | 32 |
| 29 | HOUSING_UN | 32 |
| 30 | Shape_Area | 31 |

### ArcGIS Top 100 Parameters

| Rank | Parameter | Count |
|------|-----------|-------|
| 1 | OBJECTID | 94 |
| 2 | Shape__Length | 63 |
| 3 | Shape__Area | 47 |
| 4 | NAME | 21 |
| 5 | STATE | 15 |
| 6 | GlobalID | 14 |
| 7 | url | 12 |
| 8 | lastupdate | 11 |
| 9 | FID | 11 |
| 10 | SHAPE__Area | 11 |
| 11 | COUNTY | 11 |
| 12 | SHAPE__Length | 11 |
| 13 | abbrev_name | 10 |
| 14 | lgid | 10 |
| 15 | alt_address | 10 |
| 16 | prev_name | 10 |
| 17 | lgname | 10 |
| 18 | lgstatusid | 10 |
| 19 | mail_city | 10 |
| 20 | mail_zip | 10 |
| 21 | source | 10 |
| 22 | mail_address | 10 |
| 23 | mail_state | 10 |
| 24 | lgtypeid | 10 |
| 25 | CITY | 9 |
| 26 | Direction | 9 |
| 27 | FIPS | 8 |
| 28 | HighwayNumber | 8 |
| 29 | EndRefPoint | 8 |
| 30 | City | 8 |

## SODA Top 50 Parameters
| Parameter | Count |
|-----------|-------|
| the_geom | 266 |
| emp | 87 |
| unemp | 78 |
| laborforce | 78 |
| OBJECTID | 73 |
| SHAPE | 72 |
| ESRI_OID | 72 |
| WHITE_NH | 71 |
| BLACK_NH | 71 |
| HISPANIC | 71 |
| ASIAN_NH | 71 |
| AMIND_NH | 71 |
| HAWPI_NH | 71 |
| MULTI_NH | 71 |
| OTHER_NH | 71 |
| totalparticipants | 69 |
| totalpatients | 69 |
| totaltreatmentsprovided | 69 |
| totalvisitstransactiondate | 69 |
| prov | 49 |
| date | 46 |
| name | 44 |
| id | 36 |
| identifier | 31 |
| status | 29 |
| address | 22 |
| description | 21 |
| location | 20 |
| state | 20 |
| zip | 20 |
| year | 19 |
| type | 18 |
| age | 17 |
| code | 16 |
| street | 15 |
| county | 15 |
| city | 14 |
| geom | 14 |
| title | 13 |
| phone | 13 |
| website | 12 |
| email | 11 |
| geometry | 10 |
| lat | 10 |
| lng | 10 |
| longitude | 10 |
| latitude | 10 |
| url | 10 |
| source | 10 |
| color | 9 |

## ArcGIS Top 50 Parameters
| Parameter | Count |
|-----------|-------|
| OBJECTID | 94 |
| Shape__Length | 63 |
| Shape__Area | 47 |
| NAME | 21 |
| STATE | 15 |
| GlobalID | 14 |
| url | 12 |
| COUNTY | 11 |
| lastupdate | 11 |
| SHAPE__Area | 11 |
| SHAPE__Length | 11 |
| FID | 11 |
| source | 10 |
| prev_name | 10 |
| lgstatusid | 10 |
| alt_address | 10 |
| mail_state | 10 |
| mail_zip | 10 |
| mail_address | 10 |
| lgtypeid | 10 |
| lgname | 10 |
| abbrev_name | 10 |
| mail_city | 10 |
| lgid | 10 |
| Direction | 9 |
| CITY | 9 |
| EndRefPoint | 8 |
| Highway | 8 |
| Latitude | 8 |
| Longitude | 8 |
| City | 8 |
| FIPS | 8 |
| HighwayNumber | 8 |
| STATE_NAME | 7 |
| GEOID | 7 |
| SOURCE | 7 |
| POPULATION | 7 |
| SQMI | 7 |
| INTPTLON | 6 |
| INTPTLAT | 6 |
| FUNCSTAT | 6 |
| STATE_FIPS | 6 |
| STATE_ABBR | 6 |
| State | 6 |
| ID | 6 |
| County | 6 |
| POP100 | 5 |
| HU100 | 5 |
| REGION | 5 |
| Mile_Post | 5 | 