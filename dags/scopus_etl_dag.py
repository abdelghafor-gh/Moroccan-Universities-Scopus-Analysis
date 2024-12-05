from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Get the project root directory
def get_project_root():
    """Get the project root directory"""
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    return current_dir.parent

# Add the scripts directory to Python path
project_root = get_project_root()
scripts_dir = project_root / 'scripts'
sys.path.append(str(scripts_dir))

# Import the ETL functions
from translate_affiliations import main as translate_affiliations
from prepare_cities_mapping import main as prepare_cities_mapping
from prepare_affiliation_mappers import main as prepare_affiliation_mappers
from etl import main as run_etl

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    project_root = get_project_root()
    (project_root / "data/transformed").mkdir(parents=True, exist_ok=True)
    (project_root / "mappers").mkdir(parents=True, exist_ok=True)

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(weeks=1),
}

# Create the DAG
dag = DAG(
    'scopus_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Moroccan Universities Scopus Analysis',
    schedule_interval=timedelta(days=1),  # Run daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['scopus', 'etl', 'universities'],
)

# Create directories task
create_dirs_task = PythonOperator(
    task_id='create_directories',
    python_callable=create_directories,
    dag=dag,
    doc_md="""
    # Create Directories Task
    Creates necessary directories for the pipeline:
    - data/transformed
    - mappers
    """
)

# Create tasks
translate_task = PythonOperator(
    task_id='translate_affiliations',
    python_callable=translate_affiliations,
    dag=dag,
    doc_md="""
    # Translate Affiliations Task
    Translates French institution names to English.
    
    Input: data/raw/Universities-Affiliations/Moroccan-Affiliations.csv
    Output: data/transformed/affiliations.csv
    """
)

cities_mapping_task = PythonOperator(
    task_id='prepare_cities_mapping',
    python_callable=prepare_cities_mapping,
    dag=dag,
    doc_md="""
    # Prepare Cities Mapping Task
    Creates mapping for city name variations.
    
    Input: data/raw/Universities-Affiliations/Moroccan-Affiliations.csv
    Output: mappers/cities_mapping.json
    """
)

affiliation_mappers_task = PythonOperator(
    task_id='prepare_affiliation_mappers',
    python_callable=prepare_affiliation_mappers,
    dag=dag,
    doc_md="""
    # Prepare Affiliation Mappers Task
    Creates mappings for affiliations and universities by city.
    
    Input: data/transformed/affiliations.csv
    Output: 
    - mappers/affiliations_by_city.json
    - mappers/universities_by_city.json
    """
)

etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
    doc_md="""
    # Run ETL Task
    Transforms raw Scopus data using the mapping files.
    
    Input: 
    - data/raw/scopus/2023.csv
    - All mapping files
    Output: data/transformed/transformed_23.csv
    """
)

# Define task dependencies
create_dirs_task >> translate_task >> cities_mapping_task >> affiliation_mappers_task >> etl_task
