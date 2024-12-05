import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

try:
    from snowflake.sqlalchemy import URL as snowflake_URL
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.db_type = os.getenv("DB_TYPE", "postgres").lower()
        if self.db_type not in ["postgres", "snowflake"]:
            raise ValueError(f"Unsupported database type: {self.db_type}")
        if self.db_type == "snowflake" and not SNOWFLAKE_AVAILABLE:
            raise ImportError("Snowflake support requires snowflake-sqlalchemy package. "
                            "Install it with: pip install snowflake-sqlalchemy")
        self.engine = None
        self.Session = None

    def connect(self):
        """Create database connection based on specified type"""
        if self.db_type == "postgres":
            self._connect_postgres()
        elif self.db_type == "snowflake":
            self._connect_snowflake()
        
        # Create session maker
        self.Session = sessionmaker(bind=self.engine)

    def _connect_postgres(self):
        """Connect to PostgreSQL database"""
        postgres_url = os.getenv("POSTGRES_URL")
        if not postgres_url:
            # Construct URL from individual components if full URL not provided
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            database = os.getenv("POSTGRES_DB", "scopus_analysis")
            
            postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        self.engine = create_engine(postgres_url)

    def _connect_snowflake(self):
        """Connect to Snowflake database"""
        if not SNOWFLAKE_AVAILABLE:
            raise ImportError("Snowflake support not available")
            
        # Use Snowflake's URL constructor for proper connection string formatting
        self.engine = create_engine(snowflake_URL(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            role=os.getenv("SNOWFLAKE_ROLE", "PUBLIC")  # Added role parameter
        ))

    def get_session(self):
        """Get a new database session"""
        if not self.Session:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.Session()

    def create_tables(self, Base):
        """Create all tables defined in the models"""
        if self.db_type == "snowflake":
            # Snowflake requires explicit schema creation
            schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
            with self.engine.connect() as conn:
                conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                
        Base.metadata.create_all(self.engine)

# Example usage:
if __name__ == "__main__":
    db = DatabaseConnection()
    db.connect()
    session = db.get_session()
