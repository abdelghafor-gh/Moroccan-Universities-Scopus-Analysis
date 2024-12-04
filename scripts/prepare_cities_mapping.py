import pandas as pd
import json
from unidecode import unidecode
from pathlib import Path
import os

def get_project_root():
    """Get the project root directory from the script location"""
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    return current_dir.parent

def create_directories():
    """Create necessary directories if they don't exist"""
    project_root = get_project_root()
    Path(project_root / "mappers").mkdir(parents=True, exist_ok=True)

def prepare_cities_mapping():
    # Get project root
    project_root = get_project_root()
    
    # Read affiliations data
    affiliations_df = pd.read_csv(project_root / "data/raw/Universities-Affiliations/Moroccan-Affiliations.csv")
    
    # Get unique French city names
    french_city_names = affiliations_df['City'].apply(lambda x: x.strip()).unique().tolist()
    
    # Create initial mapping
    cities_mapping = {}
    for city_fr in french_city_names:
        decoded_city_fr = unidecode(city_fr)
        # don't map correct city names
        cities_mapping[city_fr.lower()] = city_fr

        if decoded_city_fr != city_fr:
            # map decoded city name to correct
            cities_mapping[decoded_city_fr.lower()] = city_fr

    # Add other common variations
    other_cities_mapping = {
        'marrakesh': 'Marrakech',
        'mohammadia': 'Mohammedia',
        'tangier': 'Tanger',
        'fez': 'Fès',
        'fés': 'Fès',
        'méknés': 'Meknès',
        'meekness': 'Meknès',
        'quarzazate': 'Ouarzazate',
        'tetuan': 'Tétouan'
    }
    
    cities_mapping.update(other_cities_mapping)
    
    return cities_mapping

def main():
    # Create mappers directory
    create_directories()
    
    # Prepare cities mapping
    print("Preparing cities mapping...")
    cities_mapping = prepare_cities_mapping()
    
    # Save the mapping to JSON
    project_root = get_project_root()
    output_path = project_root / 'mappers/cities_mapping.json'
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(cities_mapping, json_file, ensure_ascii=False, indent=4)
    
    print(f"Cities mapping saved to {output_path}")

if __name__ == "__main__":
    main()
