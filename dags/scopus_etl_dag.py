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

# Add the project directories to Python path
project_root = get_project_root()
scripts_dir = project_root / 'scripts'
models_dir = project_root / 'models'
sys.path.extend([str(scripts_dir), str(models_dir)])

# Import the ETL functions
from translate_affiliations import main as translate_affiliations
from prepare_cities_mapping import main as prepare_cities_mapping
from prepare_affiliation_mappers import main as prepare_affiliation_mappers
from etl import main as run_etl
from combine_transformed import combine_transformed_files
from build_fact_and_dimensions import main as build_fact_dimensions
from transform_journal import main as transform_journal
from load_to_postgres import main as load_to_postgres

# Import database initialization for Airflow
# from init_db_airflow import init_database_airflow
from init_db import init_database

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    project_root = get_project_root()
    (project_root / "data/transformed").mkdir(parents=True, exist_ok=True)
    (project_root / "mappers").mkdir(parents=True, exist_ok=True)
    (project_root / "data/final").mkdir(parents=True, exist_ok=True)
    (project_root / "data/dimensions").mkdir(parents=True, exist_ok=True)

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
    - data/final
    - data/warehouse
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

transform_journal_task = PythonOperator(
    task_id='transform_journal',
    python_callable=transform_journal,
    dag=dag,
    doc_md="""
    # Transform Journal Task
    Transforms journal metadata and prepares it for the database.
    
    Input: data/raw/journal_metrics.csv
    Output: data/transformed/journal_metrics_transformed.csv
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

combine_transformed_task = PythonOperator(
    task_id='combine_transformed',
    python_callable=combine_transformed_files,
    dag=dag,
    doc_md="""
    # Combine Transformed Task
    Combines all transformed CSV files and filters invalid entries.
    
    Input: data/transformed/transformed_*.csv
    Output: data/final/combined_data.csv
    """
)

build_dimensions_task = PythonOperator(
    task_id='build_fact_dimensions',
    python_callable=build_fact_dimensions,
    dag=dag,
    doc_md="""
    # Build Fact and Dimensions Task
    Creates fact and dimension tables for the data warehouse.
    
    Input: data/final/combined_data.csv
    Output: Multiple dimension and fact tables in data/warehouse/
    """
)

init_db_task = PythonOperator(
    task_id='init_db',
    # python_callable=init_database_airflow,
    python_callable=init_database,
    op_kwargs={'is_airflow': True},
    dag=dag,
    doc_md="""
    # Initialize Database Task
    Creates the database schema and tables using Airflow-specific database initialization.
    
    Output: Initialized PostgreSQL database schema
    """
)

load_to_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    op_kwargs={'is_airflow': True},
    dag=dag,
    doc_md="""
    # Load to Postgres Task
    Loads fact and dimension tables into PostgreSQL database.
    
    Input: data/warehouse/* tables
    Output: Populated PostgreSQL database
    """
)

# trigger_load_to_postgres = TriggerDagRunOperator(
#     task_id='trigger_load_to_postgres',
#     trigger_dag_id='load_scopus_data_to_postgres',
#     dag=dag,
#     doc_md="""
#     # Trigger Load to Postgres Task
#     Triggers the dedicated DAG for loading data into PostgreSQL.
#     This DAG handles loading of all fact and dimension tables in a structured way.
    
#     Input: data/warehouse/* tables
#     Output: Populated PostgreSQL database
#     """
# )

# Define task dependencies
create_dirs_task >> translate_task >> cities_mapping_task >> affiliation_mappers_task >> transform_journal_task >> etl_task >> combine_transformed_task >> build_dimensions_task >> init_db_task >> load_to_postgres_task
