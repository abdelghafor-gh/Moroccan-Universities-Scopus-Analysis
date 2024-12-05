import logging
import pandas as pd
import json
import re
import unicodedata
from pathlib import Path
import os
from utils import get_project_root, create_directories

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_author_id_name(auth_id_name):
    """Extract author ID and name from the combined string"""
    # extract author name
    name_pattern = r"[A-Za-záéíóúÁÉÍÓÚñÑ]+,\s[A-Za-záéíóúÁÉÍÓÚñÑ]+"
    name_match = re.search(name_pattern, auth_id_name)

    # extract id
    id_match = re.search(r'\((\d+)\)', auth_id_name)
    
    if id_match and name_match:
        author_id = id_match.group(1)
        author_name = name_match.group()
        return author_id, author_name
    else:
        return None, None

def extract_country_name(affiliation_full_name):
    """Extract country name from the full affiliation string"""
    try:
        parts = affiliation_full_name.lower().split(',')
        country = parts[-1].strip().lower()
        return country
    except:
        return None

def extract_city_name(affiliation_full_name, cities_mapping):
    """Extract and map city name from the full affiliation string"""
    affiliation = affiliation_full_name.lower()
    parts = affiliation.split(',')
    
    expected_city = None
    if len(parts) > 1:
        expected_city = parts[-2].strip().lower()
        for key, value in cities_mapping.items():
            if key == expected_city:
                return value
    
    for key, value in cities_mapping.items():
        if key in affiliation:
            return value
    
    return None

def remove_accents(text):
    """Remove accents from text"""
    normalized_text = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized_text if not unicodedata.combining(char))

def normalize_digits(affiliation):
    """Normalize numerical representations in text"""
    patterns = {
        r'\b(first|1st|1er|i)\b': '1',  # Variations of 1
        r'\b(second|2nd|ii)\b': '2',    # Variations of 2
        r'\b(fifth|5th|v)\b': '5'       # Variations of 5
    }
    
    normalized_affiliation = affiliation
    for pattern, replacement in patterns.items():
        normalized_affiliation = re.sub(pattern, replacement, normalized_affiliation)
    return normalized_affiliation

def normalize_affiliation(affiliation):
    """Normalize affiliation text"""
    affiliation = affiliation.lower()
    affiliation = remove_accents(affiliation)
    affiliation = normalize_digits(affiliation)
    return affiliation

def extract_affiliation_name(affiliation_full_name, city, affiliations_by_city, universities_by_city):
    """Extract standardized affiliation name"""
    if not city:
        logging.debug(f"No city found for affiliation: {affiliation_full_name}")
        return None, None
    
    affiliation = normalize_affiliation(affiliation_full_name)
    logging.debug(f"Normalized affiliation: {affiliation}")

    if city in affiliations_by_city:
        for aff_id, variations in affiliations_by_city[city].items():
            for variation in variations:
                if variation in affiliation:
                    logging.info(f"Found affiliation match: {variations[-1]} (ID: {aff_id}) for '{affiliation_full_name}'")
                    return aff_id, variations[-1]  # Return ID and English name

    if city in universities_by_city:
        for univ_id, variations in universities_by_city[city].items():
            for variation in variations:
                if variation in affiliation:
                    logging.info(f"Found university match: {variations[-1]} (ID: {univ_id}) for '{affiliation_full_name}'")
                    return univ_id, variations[-1]  # Return ID and English name
    
    logging.warning(f"No match found for affiliation: {affiliation_full_name} in city: {city}")
import pandas as pd
import json
import re
import unicodedata
from pathlib import Path
import os
from utils import get_project_root, create_directories

def extract_author_id_name(auth_id_name):
    """Extract author ID and name from the combined string"""
    # extract author name
    name_pattern = r"[A-Za-záéíóúÁÉÍÓÚñÑ]+,\s[A-Za-záéíóúÁÉÍÓÚñÑ]+"
    name_match = re.search(name_pattern, auth_id_name)

    # extract id
    id_match = re.search(r'\((\d+)\)', auth_id_name)
    
    if id_match and name_match:
        author_id = id_match.group(1)
        author_name = name_match.group()
        return author_id, author_name
    else:
        return None, None

def extract_country_name(affiliation_full_name):
    """Extract country name from the full affiliation string"""
    try:
        parts = affiliation_full_name.lower().split(',')
        country = parts[-1].strip().lower()
        return country
    except:
        return None

def extract_city_name(affiliation_full_name, cities_mapping):
    """Extract and map city name from the full affiliation string"""
    affiliation = affiliation_full_name.lower()
    parts = affiliation.split(',')
    
    expected_city = None
    if len(parts) > 1:
        expected_city = parts[-2].strip().lower()
        for key, value in cities_mapping.items():
            if key == expected_city:
                return value
    
    for key, value in cities_mapping.items():
        if key in affiliation:
            return value
    
    return None

def remove_accents(text):
    """Remove accents from text"""
    normalized_text = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized_text if not unicodedata.combining(char))

def normalize_digits(affiliation):
    """Normalize numerical representations in text"""
    patterns = {
        r'\b(first|1st|1er|i)\b': '1',  # Variations of 1
        r'\b(second|2nd|ii)\b': '2',    # Variations of 2
        r'\b(fifth|5th|v)\b': '5'       # Variations of 5
    }
    
    normalized_affiliation = affiliation
    for pattern, replacement in patterns.items():
        normalized_affiliation = re.sub(pattern, replacement, normalized_affiliation)
    return normalized_affiliation

def normalize_affiliation(affiliation):
    """Normalize affiliation text"""
    affiliation = affiliation.lower()
    affiliation = remove_accents(affiliation)
    affiliation = normalize_digits(affiliation)
    return affiliation

def extract_affiliation_name(affiliation_full_name, city, affiliations_by_city, universities_by_city):
    """Extract standardized affiliation name"""
    if not city:
        return None, None
    
    affiliation = normalize_affiliation(affiliation_full_name)

    for key, values in affiliations_by_city[city].items():
        for val in values:
            if re.search(rf'\b{re.escape(val)}\b', affiliation):
                return key, val

    if city not in universities_by_city.keys():
        return None, None
        
    for key, values in universities_by_city[city].items():
        for val in values:
            if re.search(rf'\b{re.escape(val)}\b', affiliation):
                return key, val
    
    return None, None

def transform_data(df, cities_mapping, affiliations_by_city, universities_by_city):
    """Transform the data using the mapping files"""
    new_df = pd.DataFrame(columns=["author_id", "author_name", "affiliation_full_name", "city", "affiliation", "affiliation_id"])

    for _, row in df.iterrows():
        authors_with_ids = row["Author full names"].split(';')
        raw_affiliations = row["Affiliations"].split(';')
        
        ids, author_names, affiliations_full_name, cities, affiliations, affiliation_ids = [], [], [], [], [], []
        
        for auth_id_name, aff in zip(authors_with_ids, raw_affiliations):
            author_id, author_name = extract_author_id_name(auth_id_name)
            
            if not (author_id and author_name):
                continue

            # Extract country
            country = extract_country_name(aff)
            if country not in ["morocco", "maroc"]:
                continue
            
            # Extract city
            city = extract_city_name(aff, cities_mapping)

            # Extract affiliation and aff id
            aff_id, affiliation = extract_affiliation_name(aff, city, affiliations_by_city, universities_by_city)

            ids.append(author_id)
            author_names.append(author_name)
            affiliations_full_name.append(aff)
            cities.append(city)
            affiliation_ids.append(aff_id)
            affiliations.append(affiliation)

        data = pd.DataFrame({
            "author_id": ids,
            "author_name": author_names,
            "affiliation_full_name": affiliations_full_name,
            "city": cities,
            "affiliation": affiliations,
            "affiliation_id": affiliation_ids
        })

        new_df = pd.concat([new_df, data], ignore_index=True)
        
    return new_df

def load_mapping_files():
    """Load all mapping files"""
    project_root = get_project_root()
    
    # Load cities mapping
    with open(project_root / "mappers/cities_mapping.json", 'r', encoding='utf-8') as f:
        cities_mapping = json.load(f)
    
    # Load affiliations by city
    with open(project_root / "mappers/affiliations_by_city.json", 'r', encoding='utf-8') as f:
        affiliations_by_city = json.load(f)
    
    # Load universities by city
    with open(project_root / "mappers/universities_by_city.json", 'r', encoding='utf-8') as f:
        universities_by_city = json.load(f)
    
    return cities_mapping, affiliations_by_city, universities_by_city

def main():
    print("Loading mapping files...")
    cities_mapping, affiliations_by_city, universities_by_city = load_mapping_files()
    
    print("Reading input data...")
    project_root = get_project_root()
    df = pd.read_csv(project_root / "data/raw/scopus/2023.csv")
    
    print("Transforming data...")
    transformed_df = transform_data(df, cities_mapping, affiliations_by_city, universities_by_city)
    
    # Create output directory if it doesn't exist
    create_directories()
    
    # Save transformed data
    output_path = project_root / "data/transformed/transformed_23.csv"
    transformed_df.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")
    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()
