import pandas as pd
from pathlib import Path
from tqdm import tqdm
from utils import get_project_root

def combine_transformed_files():
    """
    Combines all transformed CSV files from data/transformed directory,
    filters out rows with empty affiliations, and saves the result.
    """
    print("\nStarting to combine transformed files...")
    
    # Get paths
    project_root = get_project_root()
    transformed_dir = project_root / "data/transformed"
    output_dir = project_root / "data/final"
    output_dir.mkdir(exist_ok=True)
    
    # Get list of all transformed CSV files
    transformed_files = list(transformed_dir.glob("transformed_*.csv"))
    
    if not transformed_files:
        print("No transformed files found in the transformed directory!")
        return
    
    print(f"Found {len(transformed_files)} transformed files to process")
    
    # Initialize an empty list to store all dataframes
    all_dfs = []
    
    # Read and combine all transformed files
    for file_path in tqdm(transformed_files, desc="Reading files", unit="file"):
        # Read CSV with affiliation_id as integer
        df = pd.read_csv(file_path, dtype={'affiliation_id': 'Int64'})
        all_dfs.append(df)
    
    print("Combining all dataframes...")
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    print("Filtering out rows with empty affiliations...")
    # Filter out rows where either affiliation or affiliation_id is empty/null
    filtered_df = combined_df.dropna(subset=['affiliation', 'affiliation_id'])
    
    # Convert affiliation_id to integer after filtering
    filtered_df['affiliation_id'] = filtered_df['affiliation_id'].astype('int')
    
    # Print statistics
    total_rows = len(combined_df)
    filtered_rows = len(filtered_df)
    removed_rows = total_rows - filtered_rows
    
    print(f"\nStatistics:")
    print(f"Total rows before filtering: {total_rows:,}")
    print(f"Rows with valid affiliations: {filtered_rows:,}")
    print(f"Rows removed: {removed_rows:,}")
    print(f"Percentage of rows kept: {(filtered_rows/total_rows*100):.2f}%")
    
    # Save the combined and filtered data
    output_path = output_dir / "combined_filtered_data.csv"
    filtered_df.to_csv(output_path, index=False)
    print(f"\nCombined and filtered data saved to: {output_path}")

if __name__ == "__main__":
    combine_transformed_files()
