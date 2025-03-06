#!/usr/bin/env python3
"""
API Parameter Analyzer

This script analyzes the metadata extracted from Soda and ArcGIS APIs to identify
the most commonly used parameters for each API type separately. It generates:
1. Word cloud visualizations of parameter frequency
2. Bar charts of the most common parameters
3. CSV files with parameter statistics
4. Detailed logs of the analysis process

Usage:
    python analyze_apis.py
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from wordcloud import WordCloud
import seaborn as sns
import logging
import re
import shutil
from urllib.parse import urlparse
import squarify
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import glob
import numpy as np

# Define folder paths
METADATA_SODA_FOLDER = "MetaDataSoda"
METADATA_ARCGIS_FOLDER = "MetaDataArcGis"
OUTPUT_FOLDER = "output"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define subfolder structure
def get_api_folders(api_type):
    """Get folder structure for a specific API type."""
    base_folder = os.path.join(OUTPUT_FOLDER, api_type.lower())
    return {
        'base': base_folder,
        'visualizations': os.path.join(base_folder, 'visualizations'),
        'interactive': os.path.join(base_folder, 'interactive'),
        'data': os.path.join(base_folder, 'data'),
        'reports': os.path.join(base_folder, 'reports'),
        'logs': os.path.join(base_folder, 'logs')
    }

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(OUTPUT_FOLDER, 'api_parameter_analysis.log'), mode='w')
    ]
)

def test_soda_metadata_structure(json_file):
    """Test and log the structure of SODA metadata files."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Log basic file info
        logging.info(f"\nAnalyzing structure of {os.path.basename(json_file)}")
        logging.info("=" * 50)
        
        # Check metadata structure
        if not isinstance(data, dict):
            logging.error(f"Invalid root structure in {json_file}. Expected dict, got {type(data)}")
            return False
            
        # Check for required fields
        required_fields = ['file_path', 'base_url', 'dataset_id', 'domain', 'metadata']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logging.error(f"Missing required fields in {json_file}: {missing_fields}")
            return False
        
        # Check columns structure
        if 'columns' not in data:
            logging.error(f"No 'columns' field found in {json_file}")
            return False
            
        if not isinstance(data['columns'], list):
            logging.error(f"'columns' is not a list in {json_file}")
            return False
        
        # Analyze column structure
        param_count = 0
        column_issues = []
        
        for i, column in enumerate(data['columns']):
            if not isinstance(column, dict):
                column_issues.append(f"Column {i} is not a dictionary")
                continue
                
            if 'name' not in column:
                column_issues.append(f"Column {i} missing 'name' field")
            else:
                param_count += 1
                
            # Log column details for debugging
            logging.debug(f"Column {i} structure: {list(column.keys())}")
        
        # Log findings
        logging.info(f"Total parameters found: {param_count}")
        if column_issues:
            logging.warning(f"Column structure issues in {json_file}:")
            for issue in column_issues:
                logging.warning(f"- {issue}")
        
        return True
    except Exception as e:
        logging.error(f"Error analyzing {json_file}: {str(e)}")
        return False

def extract_soda_parameters(json_file):
    """Extract parameters from SODA API metadata."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Use a set to ensure unique parameters per file
        unique_parameters = set()
        dataset_id = data.get('dataset_id', 'unknown')
        domain = data.get('domain', 'unknown')
        
        # Track parameter sources for debugging
        param_sources = defaultdict(list)
        
        if 'columns' in data and isinstance(data['columns'], list):
            for column in data['columns']:
                if isinstance(column, dict) and 'name' in column:
                    param_name = column['name']
                    # Add to set instead of list to ensure uniqueness
                    unique_parameters.add(param_name)
                    param_sources[param_name].append({
                        'dataset': dataset_id,
                        'domain': domain,
                        'field_type': column.get('dataTypeName', 'unknown'),
                        'description': column.get('description', 'none'),
                        'position': column.get('position', 0)
                    })
                    
                    logging.debug(f"Extracted parameter '{param_name}' from dataset {dataset_id} on domain {domain}")
        
        # Convert set to list for further processing
        parameters = list(unique_parameters)
        
        # Log parameters that appear frequently
        param_count = Counter(parameters)
        frequent_params = {p: c for p, c in param_count.items() if c >= 80}  # Track params appearing 80+ times
        if frequent_params:
            logging.info(f"Frequent parameters in {dataset_id} ({domain}):")
            for param, count in frequent_params.items():
                logging.info(f"  - {param}: {count} occurrences")
        
        # Save parameter sources for analysis
        output_dir = os.path.join('output', 'soda', 'parameter_sources')
        os.makedirs(output_dir, exist_ok=True)
        
        for param, sources in param_sources.items():
            if len(sources) >= 80:  # Track sources for frequently occurring parameters
                source_file = os.path.join(output_dir, f"{param.replace('/', '_')}_sources.json")
                with open(source_file, 'w') as f:
                    json.dump({
                        'parameter': param,
                        'occurrence_count': len(sources),
                        'sources': sources
                    }, f, indent=2)
                logging.info(f"Saved source information for frequent parameter '{param}' to {source_file}")
        
        return parameters
    except Exception as e:
        logging.error(f"Error processing {json_file}: {str(e)}")
        return []

def extract_arcgis_parameters(json_file):
    """Extract parameter names from ArcGIS metadata JSON file."""
    # Use a set to ensure unique parameters per file
    unique_parameters = set()
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Check if 'layers' exists
        if 'layers' in data:
            layers = data['layers']
            logging.info(f"Found {len(layers)} layers in {os.path.basename(json_file)}")
            
            for i, layer in enumerate(layers):
                if 'fields' in layer:
                    fields = layer['fields']
                    logging.info(f"Found {len(fields)} fields in layer {i} of {os.path.basename(json_file)}")
                    
                    for field in fields:
                        if 'name' in field and 'type' in field:
                            param_name = field['name']
                            param_type = field['type']
                            # Add to set instead of list to ensure uniqueness
                            unique_parameters.add(param_name)
                            logging.debug(f"Found parameter: {param_name} ({param_type}) in {os.path.basename(json_file)}")
    except Exception as e:
        logging.error(f"Error extracting parameters from {json_file}: {str(e)}")
    
    # Convert set to list for return
    parameters = list(unique_parameters)
    logging.info(f"Extracted {len(parameters)} unique parameters from {os.path.basename(json_file)}")
    return parameters

def analyze_folder(folder, extract_func, folders, api_type):
    """Analyze all JSON files in a folder and extract parameters."""
    # Create all folders if they don't exist
    for folder_path in folders.values():
        os.makedirs(folder_path, exist_ok=True)
    
    # Set up logging to a file in the logs folder
    log_file = os.path.join(folders['logs'], f"{api_type.lower()}_parameter_extraction.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Add the handler to the logger
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            if handler.baseFilename.endswith(f"{api_type.lower()}_parameter_extraction.log"):
                logger.removeHandler(handler)
    logger.addHandler(file_handler)
    
    all_parameters = []
    file_count = 0
    
    # Get all JSON files in the folder
    json_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
    
    for json_file in json_files:
        file_count += 1
        parameters = extract_func(json_file)
        all_parameters.extend(parameters)
        
        if not parameters:
            logging.warning(f"No parameters found in {json_file}")
    
    # Count parameter occurrences
    param_counter = Counter(all_parameters)
    
    return param_counter, file_count

def generate_visualizations(param_counts, folders, api_type):
    """Generate visualizations for parameter analysis."""
    # Convert to DataFrame and exclude parameters with exactly 83 or 77 occurrences
    all_params_df = pd.DataFrame(param_counts.items(), columns=['Parameter', 'Count'])
    filtered_params_df = all_params_df[~all_params_df['Count'].isin([83, 77])].sort_values('Count', ascending=False)
    
    # Save all parameters to CSV
    all_params_csv = os.path.join(folders['data'], f"all_{api_type.lower()}_parameters.csv")
    all_params_df.to_csv(all_params_csv, index=False)
    logging.info(f"Saved all parameters to {all_params_csv}")
    
    # Generate word cloud (using filtered parameters)
    filtered_param_counts = dict(zip(filtered_params_df['Parameter'], filtered_params_df['Count']))
    wordcloud = WordCloud(width=1200, height=800, background_color='white', max_words=300).generate_from_frequencies(filtered_param_counts)
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Most Common {api_type} Parameters (Excluding 83 and 77-Occurrence Parameters)')
    wordcloud_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_parameter_wordcloud.png")
    plt.savefig(wordcloud_file, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Saved word cloud to {wordcloud_file}")
    
    # Generate bar chart for top 30 parameters (using filtered parameters)
    top_params = filtered_params_df.head(30)
    top_params_csv = os.path.join(folders['data'], f"top_{api_type.lower()}_parameters.csv")
    top_params.to_csv(top_params_csv, index=False)
    logging.info(f"Saved top 30 parameters to {top_params_csv}")
    
    # Create bar chart
    plt.figure(figsize=(12, 10))
    ax = sns.barplot(x='Count', y='Parameter', data=top_params, palette='viridis')
    plt.title(f'Top 30 {api_type} Parameters (Excluding 83 and 77-Occurrence Parameters)')
    plt.xlabel('Frequency')
    plt.ylabel('Parameter Name')
    plt.tight_layout()
    bar_chart_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_top_parameters.png")
    plt.savefig(bar_chart_file, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Saved bar chart to {bar_chart_file}")
    
    # Create interactive bar chart with Plotly
    try:
        fig = px.bar(top_params, x='Count', y='Parameter', 
                    title=f'Top 30 {api_type} Parameters (Excluding 83 and 77-Occurrence Parameters)',
                    labels={'Count': 'Frequency', 'Parameter': 'Parameter Name'},
                    color='Count', color_continuous_scale='Viridis')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        interactive_bar_file = os.path.join(folders['interactive'], f"{api_type.lower()}_top_parameters_interactive.html")
        fig.write_html(interactive_bar_file)
        logging.info(f"Saved interactive bar chart to {interactive_bar_file}")
    except Exception as e:
        logging.error(f"Error creating interactive bar chart: {str(e)}")
        logging.info("Skipping interactive bar chart creation due to error")
    
    # Create horizontal bar chart for parameter distribution
    plt.figure(figsize=(12, 8))
    counts = filtered_params_df['Count'].values[:100]  # Use filtered parameters
    plt.hist(counts, bins=30, color='skyblue', edgecolor='black')
    plt.title(f'{api_type} Parameter Distribution (Excluding 83 and 77-Occurrence Parameters)')
    plt.xlabel('Frequency')
    plt.ylabel('Number of Parameters')
    plt.grid(axis='y', alpha=0.75)
    dist_chart_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_parameter_distribution.png")
    plt.savefig(dist_chart_file, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Saved horizontal bar chart to {dist_chart_file}")
    
    # Create treemap visualization
    plt.figure(figsize=(12, 8))
    top_params_for_treemap = filtered_params_df.head(50)  # Use filtered parameters
    squarify.plot(sizes=top_params_for_treemap['Count'], 
                  label=top_params_for_treemap['Parameter'], 
                  alpha=0.8, color=plt.cm.viridis(np.linspace(0, 1, len(top_params_for_treemap))))
    plt.axis('off')
    plt.title(f'Top 50 {api_type} Parameters Treemap (Excluding 83 and 77-Occurrence Parameters)')
    treemap_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_parameter_treemap.png")
    plt.savefig(treemap_file, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Saved treemap visualization to {treemap_file}")
    
    # Create interactive treemap with Plotly
    try:
        fig = px.treemap(top_params_for_treemap, path=['Parameter'], values='Count',
                        title=f'Top 50 {api_type} Parameters Treemap (Excluding 83 and 77-Occurrence Parameters)',
                        color='Count', color_continuous_scale='RdBu')
        interactive_treemap_file = os.path.join(folders['interactive'], f"{api_type.lower()}_parameter_treemap_interactive.html")
        fig.write_html(interactive_treemap_file)
        logging.info(f"Saved interactive treemap to {interactive_treemap_file}")
    except Exception as e:
        logging.error(f"Error creating interactive treemap: {str(e)}")
        logging.info("Skipping interactive treemap creation due to error")

def generate_report(param_counter, file_count, folders, api_type):
    """Generate a markdown report summarizing the analysis."""
    # Get parameters for the report
    all_params = pd.DataFrame(param_counter.most_common(), columns=['Parameter', 'Count'])
    total_count = sum(param_counter.values())
    
    # Add percentage column
    all_params['Percentage'] = (all_params['Count'] / len(param_counter) * 100).round(2)
    
    # Find frequencies with 10 or more parameters
    frequency_groups = all_params.groupby('Count')['Parameter'].agg(list).reset_index()
    frequency_groups['param_count'] = frequency_groups['Parameter'].apply(len)
    large_groups = frequency_groups[frequency_groups['param_count'] >= 10].sort_values('Count', ascending=False)
    
    # Remove parameters that are in large groups from the main table
    excluded_counts = set(large_groups['Count'].values)
    other_params = all_params[~all_params['Count'].isin(excluded_counts)].copy()
    
    # Create markdown report
    report_file = os.path.join(folders['reports'], f"{api_type.lower()}_parameter_report.md")
    with open(report_file, 'w') as f:
        f.write(f"# {api_type} API Parameter Analysis Report\n\n")
        f.write(f"## Overview\n\n")
        f.write(f"- Total {api_type} metadata files analyzed: {file_count}\n")
        f.write(f"- Total parameters found: {total_count:,}\n")
        f.write(f"- Unique parameter names: {len(param_counter):,}\n\n")
        
        # Add sections for large frequency groups
        if not large_groups.empty:
            f.write(f"## Parameter Groups with Common Frequencies\n\n")
            for _, group in large_groups.iterrows():
                count = group['Count']
                params = group['Parameter']
                param_count = len(params)
                
                f.write(f"### Parameters Occurring Exactly {count} Times ({param_count} parameters)\n\n")
                f.write("| Parameter | Count | Percentage |\n")
                f.write("|-----------|-------|------------|\n")
                
                percentage = round((count / total_count * 100), 2)
                for param in sorted(params):
                    f.write(f"| {param} | {count:,} | {percentage}% |\n")
                
                f.write("\n")
        
        f.write(f"## Top 20 Most Frequent Parameters (Excluding Common Groups)\n\n")
        f.write("| Rank | Parameter | Count | Percentage |\n")
        f.write("|------|-----------|-------|------------|\n")
        
        # Write top 20 parameters (excluding those in large groups)
        for i, (param, count, percentage) in enumerate(zip(other_params['Parameter'][:20], 
                                                         other_params['Count'][:20], 
                                                         other_params['Percentage'][:20]), 1):
            f.write(f"| {i} | {param} | {count:,} | {percentage}% |\n")
        
        f.write(f"\n## Visualizations\n\n")
        f.write(f"The following visualizations were generated:\n\n")
        f.write(f"- Word Cloud: `../visualizations/{api_type.lower()}_parameter_wordcloud.png`\n")
        f.write(f"- Top Parameters Bar Chart: `../visualizations/{api_type.lower()}_top_parameters.png`\n")
        f.write(f"- Parameter Distribution: `../visualizations/{api_type.lower()}_parameter_distribution.png`\n")
        f.write(f"- Parameter Treemap: `../visualizations/{api_type.lower()}_parameter_treemap.png`\n\n")
        
        f.write(f"## Interactive Visualizations\n\n")
        f.write(f"Interactive versions of the visualizations are available at:\n\n")
        f.write(f"- Interactive Bar Chart: `../interactive/{api_type.lower()}_top_parameters_interactive.html`\n")
        f.write(f"- Interactive Treemap: `../interactive/{api_type.lower()}_parameter_treemap_interactive.html`\n")
    
    # Create a summary text file
    summary_file = os.path.join(folders['reports'], f"{api_type.lower()}_parameter_summary.txt")
    with open(summary_file, 'w') as f:
        f.write(f"{api_type} API PARAMETER ANALYSIS SUMMARY\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total {api_type} metadata files analyzed: {file_count}\n")
        f.write(f"Total parameters found: {total_count:,}\n")
        f.write(f"Unique parameter names: {len(param_counter):,}\n\n")
        
        if not large_groups.empty:
            f.write("PARAMETER GROUPS WITH COMMON FREQUENCIES:\n")
            f.write("-" * 40 + "\n")
            for _, group in large_groups.iterrows():
                count = group['Count']
                params = group['Parameter']
                param_count = len(params)
                f.write(f"\nParameters occurring {count} times ({param_count} parameters):\n")
                for param in sorted(params):
                    f.write(f"- {param}\n")
            f.write("\n")
        
        f.write("TOP 20 MOST FREQUENT PARAMETERS (EXCLUDING COMMON GROUPS):\n")
        f.write("-" * 40 + "\n")
        for i, (param, count) in enumerate(zip(other_params['Parameter'][:20], other_params['Count'][:20]), 1):
            f.write(f"{i}. {param}: {count:,}\n")
    
    logging.info(f"Generated report files: {report_file}, {summary_file}")

def analyze_parameter_patterns(param_counter, folders, api_type, return_patterns=False):
    """Analyze naming patterns in parameters."""
    # Define regex patterns to look for
    patterns = {
        'id_pattern': r'.*id$|.*_id$|^id$|^id_.*',
        'date_pattern': r'.*date.*|.*time.*|.*timestamp.*',
        'name_pattern': r'.*name$|^name$|.*_name',
        'code_pattern': r'.*code$|^code$|.*_code',
        'type_pattern': r'.*type$|^type$|.*_type',
        'count_pattern': r'.*count$|^count$|.*_count',
        'status_pattern': r'.*status$|^status$|.*_status',
        'description_pattern': r'.*desc.*|.*description.*',
        'location_pattern': r'.*location.*|.*address.*|.*coord.*|.*lat.*|.*lon.*|.*lng.*',
        'value_pattern': r'.*value$|^value$|.*_value',
    }
    
    # Count parameters matching each pattern
    pattern_counts = {}
    for pattern_name, pattern in patterns.items():
        count = sum(1 for param in param_counter.keys() if re.search(pattern, param, re.IGNORECASE))
        pattern_counts[pattern_name.replace('_pattern', '')] = count
    
    # Create a bar chart of pattern counts
    plt.figure(figsize=(12, 8))
    bars = plt.bar(pattern_counts.keys(), pattern_counts.values())
    plt.title(f'{api_type} API Parameter Naming Patterns')
    plt.xlabel('Pattern')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    
    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height}', ha='center', va='bottom')
    
    plt.tight_layout()
    patterns_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_parameter_patterns.png")
    plt.savefig(patterns_file, dpi=300)
    plt.close()
    logging.info(f"Saved parameter patterns chart to {patterns_file}")
    
    # Create interactive version with Plotly
    try:
        fig = go.Figure(data=[
            go.Bar(x=list(pattern_counts.keys()), y=list(pattern_counts.values()),
                text=list(pattern_counts.values()), textposition='auto')
        ])
        fig.update_layout(
            title=f'{api_type} API Parameter Naming Patterns',
            xaxis_title='Pattern',
            yaxis_title='Count',
            height=600,
            width=900
        )
        interactive_patterns_file = os.path.join(folders['interactive'], f"{api_type.lower()}_parameter_patterns_interactive.html")
        fig.write_html(interactive_patterns_file)
        logging.info(f"Saved interactive parameter patterns chart to {interactive_patterns_file}")
    except Exception as e:
        logging.error(f"Error creating interactive parameter patterns chart: {str(e)}")
        logging.info("Skipping interactive parameter patterns chart creation due to error")
    
    if return_patterns:
        return pattern_counts
    return None

def analyze_url_patterns(metadata_folder, folders, api_type):
    """Analyze URL patterns in metadata files."""
    domains = Counter()
    path_segments = Counter()
    
    # Process each JSON file
    for json_file in glob.glob(os.path.join(metadata_folder, "*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Extract URLs
            urls = []
            if api_type == "SODA":
                if 'resource' in data and 'permalink' in data['resource']:
                    urls.append(data['resource']['permalink'])
            else:  # ArcGIS
                if 'serviceUrl' in data:
                    urls.append(data['serviceUrl'])
            
            # Parse URLs
            for url in urls:
                if url:
                    parsed_url = urlparse(url)
                    domains[parsed_url.netloc] += 1
                    
                    # Extract path segments
                    path = parsed_url.path.strip('/')
                    if path:
                        segments = path.split('/')
                        for segment in segments:
                            if segment:
                                path_segments[segment] += 1
        except Exception as e:
            logging.error(f"Error analyzing URLs in {json_file}: {str(e)}")
    
    # Save URL patterns to text file
    url_patterns_file = os.path.join(folders['reports'], f"{api_type.lower()}_url_patterns.txt")
    with open(url_patterns_file, 'w') as f:
        f.write(f"{api_type} URL PATTERN ANALYSIS\n")
        f.write("=" * 40 + "\n\n")
        
        f.write("TOP DOMAINS:\n")
        f.write("-" * 40 + "\n")
        for domain, count in domains.most_common():
            f.write(f"{domain}: {count}\n")
        
        f.write("\nTOP PATH SEGMENTS:\n")
        f.write("-" * 40 + "\n")
        for segment, count in path_segments.most_common(50):
            f.write(f"{segment}: {count}\n")
    
    # Create word cloud for path segments
    if path_segments:
        wordcloud = WordCloud(width=1200, height=800, background_color='white', max_words=100).generate_from_frequencies(path_segments)
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'{api_type} API Path Segments')
        path_wordcloud_file = os.path.join(folders['visualizations'], f"{api_type.lower()}_path_segments_wordcloud.png")
        plt.savefig(path_wordcloud_file, dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Saved path segments word cloud to {path_wordcloud_file}")
    
    logging.info(f"Saved URL patterns to {url_patterns_file}")

def analyze_parameter_frequency(param_counter, folders, api_type):
    """Analyze and log the frequency distribution of parameters."""
    # Get frequency distribution
    frequencies = Counter(param_counter.values())
    
    # Sort by frequency count (how many parameters have each occurrence count)
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    # Create frequency analysis report
    report_file = os.path.join(folders['reports'], f"{api_type.lower()}_frequency_analysis.md")
    with open(report_file, 'w') as f:
        f.write(f"# {api_type} Parameter Frequency Analysis\n\n")
        f.write("## Frequency Distribution\n\n")
        f.write("This analysis shows how many parameters appear a certain number of times.\n\n")
        f.write("| Occurrence Count | Number of Parameters | Example Parameters |\n")
        f.write("|-----------------|---------------------|-------------------|\n")
        
        for occur_count, param_count in sorted_freq[:20]:  # Show top 20 frequencies
            # Find example parameters with this occurrence count
            examples = [param for param, count in param_counter.items() if count == occur_count][:3]
            examples_str = ", ".join(examples)
            f.write(f"| {occur_count} | {param_count} | {examples_str} |\n")
        
        # Additional statistics
        total_params = sum(param_counter.values())
        unique_params = len(param_counter)
        avg_occurrences = total_params / unique_params if unique_params > 0 else 0
        
        f.write(f"\n## Statistics\n\n")
        f.write(f"- Total parameter occurrences: {total_params:,}\n")
        f.write(f"- Unique parameters: {unique_params:,}\n")
        f.write(f"- Average occurrences per parameter: {avg_occurrences:.2f}\n")
        f.write(f"- Number of different occurrence counts: {len(frequencies)}\n")
        
        # Analyze parameters with exactly 83 occurrences
        if 83 in frequencies:
            params_83 = [param for param, count in param_counter.items() if count == 83]
            f.write(f"\n## Analysis of Parameters with 83 Occurrences\n\n")
            f.write(f"There are {len(params_83)} parameters that appear exactly 83 times:\n\n")
            
            # Group parameters by potential categories
            demographic_params = [p for p in params_83 if any(term in p.lower() for term in ['age', 'race', 'gender', 'ethnic', 'population'])]
            housing_params = [p for p in params_83 if any(term in p.lower() for term in ['house', 'home', 'rent', 'housing'])]
            income_params = [p for p in params_83 if any(term in p.lower() for term in ['income', 'earnings', 'salary'])]
            other_params = [p for p in params_83 if p not in demographic_params + housing_params + income_params]
            
            f.write("### Demographic Parameters\n")
            f.write("- " + "\n- ".join(sorted(demographic_params)) + "\n\n")
            f.write("### Housing Parameters\n")
            f.write("- " + "\n- ".join(sorted(housing_params)) + "\n\n")
            f.write("### Income Parameters\n")
            f.write("- " + "\n- ".join(sorted(income_params)) + "\n\n")
            f.write("### Other Parameters\n")
            f.write("- " + "\n- ".join(sorted(other_params)) + "\n")
    
    logging.info(f"Generated frequency analysis report: {report_file}")
    return frequencies

def main():
    """Main function to run the analysis."""
    # Clear output folder if it exists
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)
    
    # Create folder structure for each API type
    for api_type in ["SODA", "ArcGIS"]:
        folders = get_api_folders(api_type)
        for folder_path in folders.values():
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created directory: {folder_path}")
    
    # Analyze SODA parameters
    soda_counter, soda_file_count = analyze_folder(
        METADATA_SODA_FOLDER, 
        extract_soda_parameters,
        get_api_folders("SODA"),
        "SODA"
    )
    
    # Generate SODA visualizations and analysis
    generate_visualizations(soda_counter, get_api_folders("SODA"), "SODA")
    generate_report(soda_counter, soda_file_count, get_api_folders("SODA"), "SODA")
    analyze_parameter_patterns(soda_counter, get_api_folders("SODA"), "SODA")
    analyze_url_patterns(METADATA_SODA_FOLDER, get_api_folders("SODA"), "SODA")
    analyze_parameter_frequency(soda_counter, get_api_folders("SODA"), "SODA")  # Added frequency analysis
    
    # Analyze ArcGIS parameters
    arcgis_counter, arcgis_file_count = analyze_folder(
        METADATA_ARCGIS_FOLDER,
        extract_arcgis_parameters,
        get_api_folders("ArcGIS"),
        "ArcGIS"
    )
    
    # Generate ArcGIS visualizations
    generate_visualizations(arcgis_counter, get_api_folders("ArcGIS"), "ArcGIS")
    generate_report(arcgis_counter, arcgis_file_count, get_api_folders("ArcGIS"), "ArcGIS")
    analyze_parameter_patterns(arcgis_counter, get_api_folders("ArcGIS"), "ArcGIS")
    analyze_url_patterns(METADATA_ARCGIS_FOLDER, get_api_folders("ArcGIS"), "ArcGIS")
    
    # Print summary
    logging.info("\n===== API PARAMETER ANALYSIS SUMMARY =====")
    logging.info(f"SODA parameters found: {sum(soda_counter.values()):,}")
    logging.info(f"SODA unique parameter names: {len(soda_counter):,}")
    logging.info(f"ArcGIS parameters found: {sum(arcgis_counter.values()):,}")
    logging.info(f"ArcGIS unique parameter names: {len(arcgis_counter):,}")
    logging.info("\nResults saved to:")
    logging.info(f"- {get_api_folders('SODA')['base']}/")
    logging.info(f"- {get_api_folders('ArcGIS')['base']}/")
    logging.info("\nAnalysis complete!")

if __name__ == "__main__":
    main() 