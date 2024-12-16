import pandas as pd
from pathlib import Path
from utils import get_project_root

def expand_issn(df):
    """Expand rows with multiple ISSN codes into separate rows"""
    # Create a list to store new rows
    expanded_rows = []
    
    for _, row in df.iterrows():
        # Split ISSN codes and remove any whitespace
        issn_list = [issn.strip() for issn in str(row['Issn']).split(',') if issn.strip()]
        
        # Create a new row for each ISSN code
        for issn in issn_list:
            new_row = row.copy()
            new_row['Issn'] = issn
            expanded_rows.append(new_row)
    
    # Create new dataframe from expanded rows
    return pd.DataFrame(expanded_rows)

def expand_categories(df):
    """Expand categories into separate rows, removing (Qx) quartile indicators"""
    categories_rows = []
    
    for _, row in df.iterrows():
        if pd.isna(row['Categories']):
            continue
            
        # Split categories and clean them
        categories = row['Categories'].split(';')
        for category in categories:
            # Remove quartile indicator and clean
            clean_category = category.split('(')[0].strip()
            if clean_category:
                categories_rows.append({
                    'ISSN': row['Issn'],
                    'Category': clean_category
                })
    
    return pd.DataFrame(categories_rows)

def main():
    """Transform the SJR journal CSV file from semicolon to comma separated format"""
    project_root = get_project_root()
    
    # Input and output paths using project root
    input_file = project_root / "data/raw/sjr/journal-23.csv"
    output_dir = project_root / "data/transformed"
    journal_output = output_dir / "clean_journal_23.csv"
    categories_output = output_dir / "journal_categories_23.csv"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read the semicolon-separated CSV file
    df = pd.read_csv(input_file, 
                     sep=';',  # Input file uses semicolon as separator
                     quoting=1,  # QUOTE_ALL for handling quoted values
                     encoding='utf-8')

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '')

    # Clean numeric data
    df['SJR'] = df['SJR'].str.replace(',', '.').astype(float)
    
    # Expand rows with multiple ISSN codes
    df = expand_issn(df)
    
    # Drop duplicates based on ISSN for journals
    df = df.drop_duplicates(subset=['Issn'], keep='first')
    
    # Create categories DataFrame
    categories_df = expand_categories(df)
    
    # Save both DataFrames
    df.to_csv(journal_output, 
              index=False,
              sep=',',  # Output file uses comma as separator
              encoding='utf-8',
              quoting=1)  # QUOTE_ALL to handle fields that contain commas
    
    categories_df.to_csv(categories_output, 
                         index=False,
                         sep=',',  # Output file uses comma as separator
                         encoding='utf-8',
                         quoting=1)  # QUOTE_ALL to handle fields that contain commas

    print(f"\nFile transformed successfully. Output saved to: {journal_output.relative_to(project_root)}")
    print(f"Categories saved to: {categories_output.relative_to(project_root)}")
    return df

if __name__ == "__main__":
    main()
