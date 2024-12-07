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

def transform_sjr_csv():
    """Transform the SJR journal CSV file from semicolon to comma separated format"""
    project_root = get_project_root()
    
    # Input and output paths using project root
    input_file = project_root / "data/raw/sjr/journal-23.csv"
    output_dir = project_root / "data/transformed"
    output_file = output_dir / "clean_journal_23.csv"

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
    
    # Drop duplicates based on ISSN
    df = df.drop_duplicates(subset=['Issn'], keep='first')
    
    # Write to new CSV file with comma separator
    df.to_csv(output_file, 
              index=False,
              sep=',',  # Output file uses comma as separator
              encoding='utf-8',
              quoting=1)  # QUOTE_ALL to handle fields that contain commas

    print(f"\nFile transformed successfully. Output saved to: {output_file.relative_to(project_root)}")
    return df

if __name__ == "__main__":
    transform_sjr_csv()
