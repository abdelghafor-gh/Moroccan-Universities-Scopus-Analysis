import pandas as pd
from pathlib import Path
from utils import get_project_root

def build_author_dimension(combined_df):
    """Build author dimension table from combined data"""
    # Get unique authors
    authors = combined_df[['Author ID', 'Author Name', 'Affiliation ID']].drop_duplicates(subset=['Author ID'], keep='first')

    # Rename columns
    authors = authors.rename(columns={
        'Author ID': 'id',
        'Author Name': 'Name',
        'Affiliation ID': 'affiliation_id'
    })
    
    return authors

def build_affiliation_dimension(affiliation_df):
    """Build affiliation dimension table from affiliations.csv"""
    # Select the defined list of columns
    required_cols = ['id', 'Affiliation', 'Abbreviation', 'University', 'City']
    affiliations = affiliation_df[required_cols].copy()
    
    return affiliations

def build_journal_dimension(journal_df):
    """Build journal dimension table"""
    # Select relevant columns
    journals = journal_df[[
        'Sourceid', 'Title', 'Issn', 'Rank', 'SJR', 'Publisher', 'Type', 'Categories',
    ]].drop_duplicates(subset=['Issn'], keep='first')
    
    # Rename columns to match schema
    journals = journals.rename(columns={
        'Sourceid': 'id',
        'Issn': 'ISSN',
    })
    
    return journals

def build_journal_categories(journal_categories_df):
    """Build journal categories dimension table"""
    # Add an auto-incrementing ID starting from 1
    journal_categories = journal_categories_df.copy()
    journal_categories['id'] = range(1, len(journal_categories) + 1)

    # Reorder columns to match schema
    journal_categories = journal_categories[['id', 'ISSN', 'Category']]
    
    return journal_categories

def build_fact_table(combined_df):
    """Build fact table by removing columns that are now in dimension tables"""
    # Select only the columns needed for the fact table
    fact_columns = [
        "Author ID", "Affiliation ID", "Title", "Year",
        "Document Type", "Source title", "DOI", "Link",
        "Language of Original Document", "ISSN", "PubMed ID", "Volume", "Issue"
    ]

    fact_table = combined_df[fact_columns].copy()

    # Rename columns to match schema
    fact_table = fact_table.rename(columns={
        'Author ID': 'author_id',
        'Affiliation ID': 'affiliation_id',
        'Document Type': 'Document_Type',
        'Source title': 'Source_Title',
        'Language of Original Document': 'Original_Language',
        'PubMed ID': 'PubMed_ID',
    })
    
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
    journal_categories_file = project_root / "data/transformed/journal_categories_23.csv"
    
    affiliations_df = pd.read_csv(affiliations_file)
    journal_df = pd.read_csv(journal_file)
    journal_categories_df = pd.read_csv(journal_categories_file)
    
    # Build dimension tables
    print("Building author dimension...")
    authors = build_author_dimension(combined_df)
    
    print("Building affiliation dimension...")
    affiliations = build_affiliation_dimension(affiliations_df)
    
    print("Building journal dimension...")
    journals = build_journal_dimension(journal_df)
    
    print("Building journal categories dimension...")
    journal_categories = build_journal_categories(journal_categories_df)
    
    # Build fact table
    print("Building fact table...")
    fact_table = build_fact_table(combined_df)
    
    # Save all tables
    print("Saving tables...")
    authors.to_csv(dimensions_dir / "authors.csv", index=False)
    affiliations.to_csv(dimensions_dir / "affiliations.csv", index=False)
    journals.to_csv(dimensions_dir / "journals.csv", index=False)
    journal_categories.to_csv(dimensions_dir / "journal_categories.csv", index=False)
    fact_table.to_csv(fact_dir / "publications_fact.csv", index=False)
    
    print("\nStar schema tables built successfully!")

if __name__ == "__main__":
    main()
