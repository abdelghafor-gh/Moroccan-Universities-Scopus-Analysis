from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.engine = None
        self.Session = None

    def connect(self):
        """Create database connection"""
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
        # Create session maker
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Get a new database session"""
        if not self.Session:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.Session()

    def create_tables(self, Base):
        """Create all tables defined in the models"""
        Base.metadata.create_all(self.engine)

# Example usage:
if __name__ == "__main__":
    db = DatabaseConnection()
    db.connect()
    session = db.get_session()
