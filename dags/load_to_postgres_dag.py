from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from pathlib import Path
import sys
from contextlib import contextmanager

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from scripts.utils import get_project_root
from models.database import DatabaseConnection
from models.schema import Publication, Journal, Author, Affiliation, JournalCategory
from scripts.load_to_postgres import load_table_to_db

# Update project root using the utility function
project_root = get_project_root()

# Create a single database connection for the DAG
db = DatabaseConnection(is_airflow=True)

def load_authors(db_connection):
    authors = pd.read_csv(project_root / "data/dimensions/authors.csv")
    load_table_to_db(authors, Author, db_connection.session)

def load_affiliations(db_connection):
    affiliations = pd.read_csv(project_root / "data/dimensions/affiliations.csv")
    load_table_to_db(affiliations, Affiliation, db_connection.session)

def load_journals(db_connection):
    journals = pd.read_csv(project_root / "data/dimensions/journals.csv")
    load_table_to_db(journals, Journal, db_connection.session)

def load_journal_categories(db_connection):
    journal_categories = pd.read_csv(project_root / "data/dimensions/journal_categories.csv")
    load_table_to_db(journal_categories, JournalCategory, db_connection.session)

def load_publications(db_connection):
    publications = pd.read_csv(project_root / "data/fact/publications_fact.csv")
    load_table_to_db(publications, Publication, db_connection.session)

@contextmanager
def database_connection():
    """Context manager for database connection"""
    try:
        db.connect()
        yield db
    finally:
        db.close()

def execute_with_connection(callable_func, **context):
    """Execute a function with database connection"""
    with database_connection() as conn:
        return callable_func(conn)

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(weeks=1),
}

# Create DAG
with DAG(
    'load_scopus_data_to_postgres',
    default_args=default_args,
    description='Load Scopus data to PostgreSQL database',
    schedule_interval=None,  # Set to None for manual triggering
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Create tasks for loading each table
    load_authors_task = PythonOperator(
        task_id='load_authors',
        python_callable=execute_with_connection,
        op_kwargs={'callable_func': load_authors},
    )

    load_affiliations_task = PythonOperator(
        task_id='load_affiliations',
        python_callable=execute_with_connection,
        op_kwargs={'callable_func': load_affiliations},
    )

    load_journals_task = PythonOperator(
        task_id='load_journals',
        python_callable=execute_with_connection,
        op_kwargs={'callable_func': load_journals},
    )

    load_journal_categories_task = PythonOperator(
        task_id='load_journal_categories',
        python_callable=execute_with_connection,
        op_kwargs={'callable_func': load_journal_categories},
    )

    load_publications_task = PythonOperator(
        task_id='load_publications',
        python_callable=execute_with_connection,
        op_kwargs={'callable_func': load_publications},
    )

    # Set dependencies
    # Load dimension tables first, then fact table
    load_affiliations_task >> load_authors_task
    [load_authors_task, load_journals_task, load_journal_categories_task] >> load_publications_task
