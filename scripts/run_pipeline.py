import subprocess
import sys
import os
from utils import get_project_root, create_directories
from dotenv import load_dotenv

def run_script(script_path):
    """Run a Python script and handle any errors"""
    print("="*50)
    print(f"Running {script_path}...")
    print("="*50)
    
    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"\nSuccessfully completed {script_path}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running {script_path}:")
        print(e)
        return False

def main():
    # Get the project root directory
    project_root = get_project_root()
    scripts_dir = project_root / "scripts"
    models_dir = project_root / "models"
    
    # Load environment variables
    load_dotenv(models_dir / '.env')
    db_type = os.getenv("DB_TYPE", "postgres")
    
    # Create all necessary directories
    create_directories()
    
    # Define the scripts to run in order
    scripts = [
        # Phase 1: Data Preparation
        scripts_dir / 'translate_affiliations.py',      # Step 1: Translate French affiliations to English
        scripts_dir / 'prepare_cities_mapping.py',      # Step 2: Create cities mapping
        scripts_dir / 'prepare_affiliation_mappers.py', # Step 3: Create affiliation mappings
        scripts_dir / 'transform_journal.py',           # Step 4: Transform journal metadata
        scripts_dir / 'etl.py',                         # Step 5: Run main ETL process
        
        # Phase 2: Data Integration
        scripts_dir / 'combine_transformed.py',         # Step 6: Combine transformed files
        scripts_dir / 'build_fact_and_dimensions.py',   # Step 7: Build star schema tables
        
        # Phase 3: Database Operations
        models_dir / 'init_db.py',                      # Step 8: Initialize database schema
        scripts_dir / 'load_to_warehouse.py'            # Step 9: Load data to database
    ]
    
    # Run each script in sequence
    for script in scripts:
        if not run_script(script):
            print(f"Pipeline failed at {script}")
            sys.exit(1)
    
    print("\n Complete ETL pipeline executed successfully!")
    print("\nData has been:")
    print("1. Extracted and transformed from source files")
    print("2. Combined and filtered for Moroccan publications")
    print("3. Organized into star schema structure")
    print(f"4. Loaded into {db_type.upper()} database")

if __name__ == "__main__":
    main()
