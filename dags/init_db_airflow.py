import sys
import os
from pathlib import Path

# Get the project root directory and add models to path
project_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
models_dir = project_root / 'models'
sys.path.append(str(models_dir))

from database import DatabaseConnection
from schema import Base

def init_database_airflow():
    """Initialize the database schema for Airflow environment"""
    try:
        # Create database connection with Docker container configuration
        db = DatabaseConnection(is_airflow=True)
        db.connect()
        
        # Drop all tables
        Base.metadata.drop_all(db.engine)
        print("✅ Existing tables dropped successfully!")
        
        # Create all tables defined in schema.py
        Base.metadata.create_all(db.engine)
        print("✅ Database schema created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating database schema: {str(e)}")
        raise

if __name__ == "__main__":
    init_database_airflow()
