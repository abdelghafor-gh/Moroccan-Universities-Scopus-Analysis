import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from utils import get_project_root
from models.database import DatabaseConnection
from models.schema import Publication, Journal, Author, Affiliation, JournalCategory
from dotenv import load_dotenv
from sqlalchemy import inspect

def get_required_columns(table_class):
    """Get required (non-nullable) columns from SQLAlchemy model"""
    inspector = inspect(table_class)
    return {col.key for col in inspector.columns if not col.nullable}

def clean_data(df, table_class):
    """Clean data and ensure required columns have values"""
    # Normalize column names to match schema
    df.columns = [col.lower() for col in df.columns]
    df = df.replace({np.nan: None, 'NaN': None, 'nan': None})
    
    # Get required columns
    required_cols = get_required_columns(table_class)
    
    # Get column mappings from schema
    column_map = {c.key.lower(): c.key for c in table_class.__table__.columns}
    
    # Map column names
    df.columns = [column_map.get(col.lower(), col) for col in df.columns]
    
    # Ensure required columns have values
    for col in required_cols:
        if col in df.columns and df[col].isnull().any():
            print(f" Found null values in required column '{col}'. Setting defaults...")
            if col == 'id':
                # Generate sequential IDs for null values
                null_mask = df[col].isnull()
                df.loc[null_mask, col] = range(1, null_mask.sum() + 1)
            else:
                # For other columns, use appropriate defaults
                df[col] = df[col].fillna('')
    
    return df

def load_to_warehouse(df, table_class, session, db_type, chunk_size=1000):
    """Load data to warehouse"""
    table_name = table_class.__tablename__
    total_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size else 0)
    
    # Clean data before chunking
    df = clean_data(df, table_class)
    
    for i in tqdm(range(0, len(df), chunk_size), total=total_chunks, desc=f"Loading {table_name}"):
        chunk = df.iloc[i:i + chunk_size].copy()
        
        try:
            if db_type == "snowflake":
                # For Snowflake, use SQLAlchemy Core
                table = table_class.__table__
                session.execute(table.insert(), chunk.to_dict('records'))
            else:
                # For PostgreSQL, use bulk_save_objects
                records = chunk.to_dict('records')
                instances = [table_class(**record) for record in records]
                session.bulk_save_objects(instances)
            
            session.commit()
                
        except Exception as e:
            print(f"\n Error loading {table_name}: {str(e)}")
            print("\nProblem data sample:")
            print(chunk.head())
            print("\nColumns in data:", list(chunk.columns))
            session.rollback()
            raise

def main(is_airflow=False):
    # Get paths
    project_root = get_project_root()
    models_dir = project_root / "models"
    dimensions_dir = project_root / "data/dimensions"
    fact_dir = project_root / "data/fact"
    
    # Load environment variables
    load_dotenv(models_dir / '.env')
    db_type = os.getenv("DB_TYPE", "postgres")
    
    print(f"\nLoading data to '{db_type.upper()}' database...")
    
    try:
        # Read all tables with string handling for all columns
        print("Reading data files...")
        authors = pd.read_csv(dimensions_dir / "authors.csv", dtype=str)
        affiliations = pd.read_csv(dimensions_dir / "affiliations.csv", dtype=str)
        journals = pd.read_csv(dimensions_dir / "journals.csv", dtype=str)
        journal_categories = pd.read_csv(dimensions_dir / "journal_categories.csv", dtype=str)
        publications = pd.read_csv(fact_dir / "publications_fact.csv", dtype=str)
        
        # Connect to database
        print("Connecting to database...")
        db = DatabaseConnection(is_airflow=is_airflow)
        db.connect()
        session = db.Session()
        
        try:
            # Load dimension tables
            print("\nLoading dimension tables...")
            load_to_warehouse(journals, Journal, session, db_type)
            load_to_warehouse(journal_categories, JournalCategory, session, db_type)
            load_to_warehouse(affiliations, Affiliation, session, db_type)
            load_to_warehouse(authors, Author, session, db_type)
            
            # Load fact table
            print("\nLoading fact table...")
            load_to_warehouse(publications, Publication, session, db_type)
            
            print("\n All tables loaded successfully!")
            
        except Exception as e:
            print(f"\n Error loading data: {str(e)}")
            raise
        finally:
            session.close()
            
    except Exception as e:
        print(f"\n Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
