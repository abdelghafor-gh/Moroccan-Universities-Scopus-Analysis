from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path
import snowflake.connector
from snowflake.sqlalchemy import URL

class DatabaseConnection:
    def __init__(self, is_airflow=False):
        self.engine = None
        self.Session = None
        self.is_airflow = is_airflow
        
        if not is_airflow:
            # Load environment variables from models/.env file for local development
            models_dir = Path(__file__).parent
            env_path = models_dir / '.env'
            load_dotenv(env_path)
        else:
            # Load environment variables from root .env for Airflow
            project_root = Path(__file__).parent.parent
            env_path = project_root / 'airflow-docker'/ '.env'
            load_dotenv(env_path)

    def connect(self):
        """Create database connection"""
        db_type = os.getenv("DB_TYPE", "postgres")
        
        if db_type == "postgres":
            self._connect_postgres()
        elif db_type == "snowflake":
            self._connect_snowflake()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _connect_postgres(self):
        """Create PostgreSQL database connection"""
        if self.is_airflow:
            # Use Docker container configuration when running in Airflow
            user = os.getenv("POSTGRES_USER", "airflow")
            password = os.getenv("POSTGRES_PASSWORD", "airflow")
            host = os.getenv("POSTGRES_HOST", "postgres")  # Docker service name
            port = os.getenv("POSTGRES_PORT", "5432")      # Internal Docker port
            database = "scopus_analysis"  # Always use scopus_analysis for our schema
        else:
            # Use local configuration from models/.env
            user = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "postgres")
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            database = os.getenv("POSTGRES_DB", "scopus_analysis")
        
        postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        print(f"Connecting to PostgreSQL database with URL: {postgres_url}")
        
        self.engine = create_engine(postgres_url)
        self.Session = sessionmaker(bind=self.engine)

    def _connect_snowflake(self):
        """Create Snowflake database connection"""
        # account_url = os.getenv("SNOWFLAKE_ACCOUNT")
        # # Extract account identifier from the full URL (format: account-id.region.snowflakecomputing.com)
        # account = account_url.split('.')[0] if account_url else None
        
        account = os.getenv("SNOWFLAKE_ACCOUNT")
        user = os.getenv("SNOWFLAKE_USER")
        password = os.getenv("SNOWFLAKE_PASSWORD")
        database = os.getenv("SNOWFLAKE_DATABASE")
        schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

        print(f"Connecting with account: {account}")
        
        snowflake_url = URL(
            account=account,
            user=user,
            password=password,
            database=database,
            schema=schema,
            warehouse=warehouse
        )
        
        print(f"Connecting to Snowflake database: {database}.{schema}")
        
        self.engine = create_engine(snowflake_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Get a new database session"""
        if not self.Session:
            self.connect()
        return self.Session()

    def create_tables(self, Base):
        """Create all tables defined in the models"""
        Base.metadata.create_all(self.engine)

# Example usage:
if __name__ == "__main__":
    # When running locally
    db = DatabaseConnection(is_airflow=False)
    db.connect()
    session = db.get_session()
