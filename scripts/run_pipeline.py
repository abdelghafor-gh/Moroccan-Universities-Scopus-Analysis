import subprocess
import sys
from pathlib import Path
import os
from utils import get_project_root

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
    
    # Create necessary directories
    (project_root / "data" / "transformed").mkdir(parents=True, exist_ok=True)
    (project_root / "mappers").mkdir(parents=True, exist_ok=True)
    
    # Define the scripts to run in order
    scripts = [
        scripts_dir / 'translate_affiliations.py',      # Step 1: Translate French affiliations to English
        scripts_dir / 'prepare_cities_mapping.py',      # Step 2: Create cities mapping
        scripts_dir / 'prepare_affiliation_mappers.py', # Step 3: Create affiliation mappings
        scripts_dir / 'etl.py'                          # Step 4: Run main ETL process
    ]
    
    # Run each script in sequence
    for script in scripts:
        if not run_script(script):
            print(f"Pipeline failed at {script}")
            sys.exit(1)
    
    print("\nETL pipeline completed successfully!")

if __name__ == "__main__":
    main()
