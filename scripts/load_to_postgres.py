import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from tqdm import tqdm
from utils import get_project_root
from models.database import DatabaseConnection
from models.schema import Publication, Journal, Author, Affiliation

def load_table_to_db(df, table_class, session, chunk_size=1000):
    """Load a dataframe to database table in chunks"""
    total_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size else 0)
    
    for i in tqdm(range(0, len(df), chunk_size), total=total_chunks, desc=f"Loading {table_class.__tablename__}"):
        chunk = df.iloc[i:i + chunk_size]
        
        # Convert chunk to list of dictionaries
        records = chunk.to_dict('records')
        
        # Create model instances
        instances = [table_class(**record) for record in records]
        
        # Add all instances to session
        session.bulk_save_objects(instances)
        
        # Commit the chunk
        session.commit()

def main():
    print("\nLoading data to PostgreSQL database...")
    
    # Get paths
    project_root = get_project_root()
    dimensions_dir = project_root / "data/dimensions"
    fact_dir = project_root / "data/fact"
    
    # Read the prepared tables
    print("Reading prepared tables...")
    authors = pd.read_csv(dimensions_dir / "authors.csv")
    affiliations = pd.read_csv(dimensions_dir / "affiliations.csv")
    journals = pd.read_csv(dimensions_dir / "journals.csv")
    publications = pd.read_csv(fact_dir / "publications_fact.csv")
    
    # Connect to database
    print("Connecting to database...")
    db = DatabaseConnection()
    db.connect()
    
    # Create a session
    Session = db.Session
    session = Session()
    
    try:
        # Load dimension tables first
        print("\nLoading dimension tables...")
        load_table_to_db(authors, Author, session)
        load_table_to_db(affiliations, Affiliation, session)
        load_table_to_db(journals, Journal, session)
        
        # Load fact table
        print("\nLoading fact table...")
        load_table_to_db(publications, Publication, session)
        
        print("\n✅ All tables loaded successfully!")
        
    except Exception as e:
        print(f"\n❌ Error loading tables: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
