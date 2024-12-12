# 🔄 ETL Process Documentation

## 🎯 Overview
This document describes the Extract, Transform, Load (ETL) pipeline for the Moroccan Universities Scopus Analysis project. The pipeline processes publication data from Scopus and transforms it into a structured star schema for analysis.

## 📋 Pipeline Architecture

### Pipeline Phases
The ETL pipeline is divided into three main phases:

1. **📥 Data Preparation**
   - Translation of French affiliations to English
   - Creation of mapping files for cities and institutions
   - Main ETL transformations

2. **🔧 Data Integration**
   - Combination of transformed files
   - Construction of star schema dimensions and fact tables

3. **📤 Database Operations**
   - Schema initialization
   - Data loading into PostgreSQL

## 📊 Detailed Process Flow

### Phase 1: Data Preparation

#### Step 1: Translate Affiliations (`translate_affiliations.py`)
- Translates French institution names to English
- Ensures consistency in institution naming
- Handles special characters and accents

#### Step 2: Cities Mapping (`prepare_cities_mapping.py`)
- Creates standardized mapping for Moroccan cities
- Handles variations in city names
- Maps cities to their standard forms

#### Step 3: Affiliation Mapping (`prepare_affiliation_mappers.py`)
- Creates mapping files for institutions
- Standardizes institution names
- Links institutions to their cities
- Handles variations and abbreviations

#### Step 4: Main ETL Process (`etl.py`)
- Extracts data from source files
- Performs key transformations:
  - Author information extraction
  - Affiliation standardization
  - City and country extraction
  - Data cleaning and normalization

### Phase 2: Data Integration

#### Step 5: Data Combination (`combine_transformed.py`)
- Merges transformed data files
- Ensures data consistency
- Handles duplicates and conflicts

#### Step 6: Star Schema Construction (`build_fact_and_dimensions.py`)
- Creates dimension tables:
  - Authors
  - Journals
  - Affiliations
- Builds fact table (Publications)
- Establishes relationships between tables

### Phase 3: Database Operations

#### Step 7: Schema Initialization (`init_db.py`)
- Creates database schema
- Sets up tables and relationships
- Establishes constraints and indexes

#### Step 8: Data Loading (`load_to_postgres.py`)
- Loads transformed data into PostgreSQL
- Validates data integrity
- Handles loading errors

## 📈 Data Transformations

### Key Transformation Functions

1. **Author Information**
   ```python
   def extract_author_id_name(auth_id_name):
       # Extracts author ID and name from combined string
       # Returns: (author_id, author_name)
   ```

2. **Affiliation Processing**
   ```python
   def extract_affiliation_name(affiliation_full_name, city, mappings):
       # Standardizes institution names
       # Maps to correct city
       # Returns: standardized_name
   ```

3. **Text Normalization**
   ```python
   def normalize_affiliation(text):
       # Removes accents
       # Standardizes format
       # Returns: normalized_text
   ```

## 🚨 Error Handling and Logging

- Comprehensive logging throughout the pipeline
- Error tracking and reporting
- Progress monitoring using tqdm
- Graceful failure handling

## 🏃‍♂️ Running the Pipeline

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Required Python packages (see requirements.txt)
- Source data files in correct format

### Execution
To run the complete pipeline:
```bash
python scripts/run_pipeline.py
```

### Monitoring
- Progress is logged to console
- Each step reports success/failure
- Detailed logs available for debugging

## 📊 Data Quality Checks

1. **Pre-transformation Validation**
   - Source file completeness
   - Required fields presence
   - Data format verification

2. **Post-transformation Validation**
   - Data consistency checks
   - Relationship integrity
   - Missing value handling

## 🔧 Maintenance and Updates

### Adding New Data Sources
1. Place new data files in `data/raw/`
2. Update mapping files if needed
3. Run the pipeline

### Troubleshooting
- Check logs in case of failures
- Verify source data format
- Ensure all mapping files are up to date

## 📈 Performance Considerations

- Batch processing for large datasets
- Optimized database operations
- Progress tracking for long-running operations

## 📈 Future Improvements

- [ ] Parallel processing for large datasets
- [ ] Incremental updates
- [ ] Advanced error recovery
- [ ] Real-time monitoring dashboard

## 📈 Processing New Scopus Data

### Overview
The pipeline is designed to automatically process new Scopus data files. This section explains how to add new data and run the pipeline to update your database.

### Step-by-Step Guide

1. **Prepare New Data**
   - Export your new data from Scopus in CSV format
   - Ensure it follows the standard Scopus export format
   - File naming convention: `scopus_export_YYYY.csv`

2. **Place Files in Raw Data Directory**
   ```
   data/
   └── raw/
       └── scopus/
           ├── scopus_export_2021.csv
           ├── scopus_export_2022.csv
           └── scopus_export_2023.csv  # New file
   ```

3. **Run the Pipeline**
   ```bash
   python scripts/run_pipeline.py
   ```
   The pipeline will:
   - Detect new files automatically
   - Apply all necessary transformations
   - Update the database with new records

### What Happens Behind the Scenes

1. **Data Detection**
   - Pipeline scans `data/raw/scopus/` directory
   - Identifies new and updated files
   - Prepares them for processing

2. **Automatic Processing**
   - Translation of non-English content
   - Standardization of institution names
   - City and affiliation mapping
   - Data cleaning and validation

3. **Database Updates**
   - New records are added
   - Existing records are updated if needed
   - Relationships are maintained
   - Data integrity is preserved

### Monitoring Progress

The pipeline provides real-time feedback:
```
========================================
Running translate_affiliations.py...
========================================
Processing new files...
[████████████████████] 100% Complete

========================================
Running prepare_cities_mapping.py...
========================================
[████████████████████] 100% Complete
...
```

### Validation Checks

The pipeline performs automatic validation:
1. File format verification
2. Required fields presence
3. Data consistency checks
4. Relationship integrity

### Troubleshooting

If you encounter issues:

1. **File Format Issues**
   - Ensure CSV files are properly formatted
   - Check for special characters in headers
   - Verify date formats match expected pattern

2. **Missing Data**
   - Confirm all required fields are present
   - Check for empty or null values
   - Verify reference data exists

3. **Processing Errors**
   - Check the logs for specific error messages
   - Verify file permissions
   - Ensure database connection is active

### Best Practices

1. **Before Adding New Data**
   - Backup existing database
   - Verify file formats
   - Check disk space

2. **During Processing**
   - Monitor the console output
   - Check log files
   - Verify intermediate files are created

3. **After Processing**
   - Validate new entries in database
   - Check data relationships
   - Verify data quality

### Example Timeline

```
T+0: Place new file in raw/scopus/
T+1: Run pipeline
T+2: Automatic translation starts
T+3: City/affiliation mapping
T+4: Main ETL processing
T+5: Data integration
T+6: Database update
T+7: Validation complete
```

### Recovery Procedures

If the pipeline fails:
1. Check the error logs
2. Fix any identified issues
3. Clean up temporary files
4. Restart the pipeline

The pipeline is idempotent, meaning it can be safely rerun without creating duplicates or corrupting existing data.
