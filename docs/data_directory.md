# 📂 Data Directory Documentation

## 🎯 Overview
This document provides a comprehensive guide to the data directory structure and the data flow in the Moroccan Universities Scopus Analysis project. The data processing follows a sequential path through various stages, from raw data to the final star schema model.

## 📁 Directory Structure

```
data/
├── 📥 raw/                      # Original source data
│   ├── Universities-Affiliations/
│   │   └── Moroccan-Affiliations.csv
│   ├── scopus/              # Scopus export files
│   ├── sjr/                 # Journal metrics data
│   └── ensupp/              # Additional data sources
├── 🔄 transformed/             # Cleaned and standardized data
├── ✨ final/                   # Combined and validated data
├── 📊 dimensions/              # Dimension tables
└── 📋 fact/                    # Fact tables
```

## 📦 Data Flow Timeline

### 1. 📥 Raw Data Stage (`/raw`)
- **Input Location**: `data/raw/`
- **Contents**:
  - `Universities-Affiliations/`: Moroccan universities and institutions data
    - `Moroccan-Affiliations.csv`: Master list of Moroccan institutions
  - `scopus/`: Raw Scopus publication exports
  - `sjr/`: Journal metrics and rankings
  - `ensupp/`: Supplementary data sources

#### 📝 File Formats
- CSV files with original headers
- Potentially inconsistent naming conventions
- May contain special characters or multiple languages

### 2. 🔄 Transformation Stage (`/transformed`)
- **Input**: Files from `/raw`
- **Output Location**: `data/transformed/`
- **Files**:
  - `affiliations.csv`: Standardized institution names
  - `clean_journal_23.csv`: Processed journal data
  - `transformed_2021.csv`: Cleaned 2021 publications
  - `transformed_2022.csv`: Cleaned 2022 publications
  - `transformed_2023.csv`: Cleaned 2023 publications

#### 🔧 Transformations Applied
- Text normalization
- Language standardization
- Data cleaning and validation
- Format standardization

### 3. ✨ Integration Stage (`/final`)
- **Input**: Files from `/transformed`
- **Output Location**: `data/final/`
- **Purpose**: 
  - Combines transformed files
  - Resolves conflicts
  - Ensures data consistency
  - Prepares for star schema split

### 4. 📊 Star Schema Stage
#### 📋 Dimension Tables (`/dimensions`)
- **Location**: `data/dimensions/`
- **Files**:
  - `affiliations.csv`: Institution dimension
  - `authors.csv`: Author dimension
  - `journals.csv`: Journal dimension

#### 📊 Fact Table (`/fact`)
- **Location**: `data/fact/`
- **Contents**: Publication facts with foreign keys to dimensions

## 📈 Data Quality Standards

### 📥 Raw Data
- Original, unmodified files
- Preserved in original format
- Versioned if updates received

### 🔄 Transformed Data
- Standardized formats
- Cleaned and validated
- Consistent naming conventions
- Mapped to standard values

### ✨ Final Data
- Fully validated
- Referential integrity maintained
- Ready for analytical queries

## 📝 File Naming Conventions

### 📥 Raw Files
- Original names preserved
- Date suffixes if multiple versions exist

### 🔄 Transformed Files
- Format: `transformed_YYYY.csv`
- Clear indication of content type

### 📋 Dimension and Fact Tables
- Named after the entity they represent
- Consistent with schema documentation

## 📁 Data Retention Policy

1. 📥 **Raw Data**
   - Retained indefinitely
   - Archived after processing

2. 🔄 **Transformed Data**
   - Kept for validation
   - Can be regenerated from raw

3. ✨ **Final and Schema Data**
   - Active storage
   - Regular backups maintained

## 📊 Usage Guidelines

### 📂 Accessing Raw Data
```bash
# Example path to raw Moroccan affiliations
data/raw/Universities-Affiliations/Moroccan-Affiliations.csv
```

### 🔄 Working with Transformed Data
```bash
# Latest transformed publications
data/transformed/transformed_2023.csv
```

### 📊 Using Star Schema Tables
```bash
# Dimension tables
data/dimensions/[table_name].csv

# Fact table
data/fact/publications.csv
```

## 🔄 Data Update Process

1. Place new raw data in appropriate `/raw` subdirectory
2. Run transformation scripts
3. Verify transformed output
4. Run integration process
5. Update star schema tables

## 🔍 Monitoring and Maintenance

### 📊 Size Monitoring
- Regular checks on directory sizes
- Cleanup of temporary files
- Archival of old versions

### 📈 Data Quality Checks
- Validation after each transformation
- Integrity checks before loading
- Regular audits of final data

## 📚 Related Documentation
- ETL Process: [etl_process.md](etl_process.md)
- Data Model: [data_model.md](data_model.md)
- Schema Documentation: See `models/schema.py`
