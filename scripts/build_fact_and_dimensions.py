import pandas as pd
from pathlib import Path
from utils import get_project_root

def build_author_dimension(combined_df):
    """Build author dimension table from combined data"""
    # Get unique authors
    authors = combined_df[['Author ID', 'Author Name']].drop_duplicates(subset=['Author ID'], keep='first')

    # Rename columns
    authors = authors.rename(columns={
        'Author ID': 'id',
        'Author Name': 'name'
        })
    
    return authors

def build_affiliation_dimension(affiliation_df):
    """Build affiliation dimension table from affiliations.csv"""
    # Assuming affiliations.csv has the structure we need
    affiliations = affiliation_df.copy()
    
    # Ensure required columns exist
    required_cols = ['id', 'Affiliation', 'Abbreviation', 'University', 'City']
    if not all(col in affiliations.columns for col in required_cols):
        raise ValueError(f"Affiliations file must contain columns: {required_cols}")
    
    return affiliations

def build_journal_dimension(journal_df):
    """Build journal dimension table from clean_journal_23.csv"""
    # Select and rename relevant columns
    journals = journal_df[[
        'Sourceid', 'Title', 'Issn', 'Rank', 'SJR', 'Publisher', 'Type', 'Areas'
    ]].copy()
    
    # Rename columns to match schema
    journals = journals.rename(columns={
        'Sourceid': 'ID',
    })
    
    return journals

def build_fact_table(combined_df):
    """Build fact table by removing columns that are now in dimension tables"""
    # Select only the columns needed for the fact table
    fact_columns = [
        "Author ID", "Affiliation ID", "Title", "Year",
        "Document Type", "Source title", "DOI", "Link",
        "Language of Original Document", "ISSN", "PubMed ID", "Volume", "Issue"
    ]
    
    fact_table = combined_df[fact_columns].copy()
    return fact_table

def main():
    print("\nBuilding dimension tables for star schema...")
    
    # Get paths
    project_root = get_project_root()
    transformed_dir = project_root / "data/transformed"
    final_dir = project_root / "data/final"
    fact_dir = project_root / "data/fact"
    dimensions_dir = project_root / "data/dimensions"
    fact_dir.mkdir(exist_ok=True)
    dimensions_dir.mkdir(exist_ok=True)
    
    # Read the combined transformed data
    print("Reading combined transformed data...")
    combined_file = final_dir / "combined_publications.csv"
    combined_df = pd.read_csv(combined_file)
    
    # Read supporting files
    print("Reading supporting files...")
    affiliations_file = transformed_dir / "affiliations.csv"
    journal_file = transformed_dir / "clean_journal_23.csv"
    
    affiliations_df = pd.read_csv(affiliations_file)
    journal_df = pd.read_csv(journal_file)
    
    # Build dimension tables
    print("Building author dimension...")
    authors = build_author_dimension(combined_df)
    
    print("Building affiliation dimension...")
    affiliations = build_affiliation_dimension(affiliations_df)
    
    print("Building journal dimension...")
    journals = build_journal_dimension(journal_df)
    
    # Build fact table
    print("Building fact table...")
    fact_table = build_fact_table(combined_df)
    
    # Save all tables
    print("Saving tables...")
    authors.to_csv(dimensions_dir / "authors.csv", index=False)
    affiliations.to_csv(dimensions_dir / "affiliations.csv", index=False)
    journals.to_csv(dimensions_dir / "journals.csv", index=False)
    fact_table.to_csv(fact_dir / "publications_fact.csv", index=False)
    
    print("\nStar schema tables built successfully!")

if __name__ == "__main__":
    main()
