from database import DatabaseConnection
from schema import Base

def init_database():
    """Initialize the database and create all tables"""
    try:
        # Create database connection
        db = DatabaseConnection()
        db.connect()
        
        # Create all tables defined in schema.py
        Base.metadata.create_all(db.engine)
        print("✅ Database schema created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating database schema: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()
