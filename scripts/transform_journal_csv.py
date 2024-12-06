import pandas as pd
from pathlib import Path
from utils import get_project_root

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
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '').str.lower()

    # Write to new CSV file with comma separator
    df.to_csv(output_file, 
              index=False,
              sep=',',  # Output file uses comma as separator
              encoding='utf-8',
              quoting=1)  # QUOTE_ALL to handle fields that contain commas

    print(f"File transformed successfully. Output saved to: {output_file}")
    return df

if __name__ == "__main__":
    transform_sjr_csv()
