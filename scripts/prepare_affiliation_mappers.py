import json
import pandas as pd
import unicodedata
import re
from collections import defaultdict
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

def remove_accents(text):
    """Remove accents from text"""
    normalized_text = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized_text if not unicodedata.combining(char))

def generate_en_affiliations_variations(affiliation_en):
    """Generate English variations of affiliation names"""
    variations = []
    opt1 = 'faculty of sciences and techniques'
    opt2 = 'faculty of sciences'
    opt3 = 'polydisciplinary'

    if opt1 in affiliation_en:
        v1 = affiliation_en.replace(opt1, 'faculty of science and techniques')
        v2 = affiliation_en.replace(opt1, 'faculty of sciences and technology')
        v3 = affiliation_en.replace(opt1, 'faculty of science and technology')
        variations.extend([v1, v2, v3])
    
    elif opt2 in affiliation_en:
        v = affiliation_en.replace(opt2, 'faculty of science')
        variations.append(v)
    
    elif opt3 in affiliation_en:
        u = affiliation_en.replace(opt3, 'multidisciplinary')
        variations.append(u)

    return variations

def update_affiliation(df):
    """Update specific affiliations with standardized names"""
    updated_rows = []

    # FS Semlalia -> FS
    fs_semlalia = df.loc[df['id'] == 23].copy()
    fs_semlalia.loc[:, 'Abbreviation'] = 'FS'
    fs_semlalia.loc[:, 'Affiliation'] = 'Faculté des Sciences'
    fs_semlalia.loc[:, 'Affiliation En Name'] = 'Faculty of Sciences'
    updated_rows.append(fs_semlalia)

    # FS Dhar El Mahraz -> FS
    fs_fes = df.loc[df['id'] == 153].copy()
    fs_fes.loc[:, 'Abbreviation'] = 'FS'
    fs_fes.loc[:, 'Affiliation'] = 'Faculté des Sciences'
    fs_fes.loc[:, 'Affiliation En Name'] = 'Faculty of Sciences'
    updated_rows.append(fs_fes)

    # FST Sais -> FST
    fst_fes = df.loc[df['id'] == 155].copy()
    fst_fes.loc[:, 'Abbreviation'] = 'FST'
    fst_fes.loc[:, 'Affiliation'] = 'Faculté des Sciences et Techniques'
    fst_fes.loc[:, 'Affiliation En Name'] = 'Faculty of Sciences and Techniques'
    updated_rows.append(fst_fes)

    # FST Guéliz -> FST
    fst_guez = df.loc[df['id'] == 25].copy()
    fst_guez.loc[:, 'Abbreviation'] = 'FST'
    fst_guez.loc[:, 'Affiliation'] = 'Faculté des Sciences et Techniques'
    fst_guez.loc[:, 'Affiliation En Name'] = 'Faculty of Sciences and Techniques'
    updated_rows.append(fst_guez)

    # Combine original DataFrame with the new rows
    updated_df = pd.concat([df] + updated_rows, ignore_index=True)
    return updated_df

def prepare_affiliation_mappers(affiliations_df):
    """Prepare mappings for affiliations and universities by city"""
    affiliations_by_city = defaultdict(lambda: defaultdict(list))
    universities_by_city = defaultdict(lambda: defaultdict(list))

    for _, row in affiliations_df.iterrows():
        # id
        id = row['id']
        # abbreviation
        abbreviation = row['Abbreviation'].strip().lower()
        # affiliation_en
        affiliation_en = row['Affiliation En Name'].strip().lower()
        affiliation_en = normalize_digits(affiliation_en)
        # affiliation_fr
        affiliation_fr = row['Affiliation'].strip().lower()
        affiliation_fr = remove_accents(affiliation_fr)
        affiliation_fr = normalize_digits(affiliation_fr)
        # city
        city = row['City'].strip()

        if row['Abbreviation'][0] == 'U':
            # University
            universities_by_city[city][id].append(abbreviation)
            universities_by_city[city][id].append(affiliation_fr)
            universities_by_city[city][id].append(affiliation_en)

            # Add variations of English names
            affiliation_en_2 = ' '.join([affiliation_en.rsplit(' ', 1)[1], affiliation_en.rsplit(' ', 1)[0]])
            affiliation_en_3 = ' of '.join([affiliation_en.rsplit(' ', 1)[1], affiliation_en.rsplit(' ', 1)[0]])
            universities_by_city[city][id].append(affiliation_en_2)
            universities_by_city[city][id].append(affiliation_en_3)
        else:
            # Affiliation
            affiliations_by_city[city][id].append(abbreviation)
            affiliations_by_city[city][id].append(affiliation_fr)
            affiliations_by_city[city][id].append(affiliation_en)
            # Add variations
            en_variations = generate_en_affiliations_variations(affiliation_en)
            affiliations_by_city[city][id].extend(en_variations)

    return dict(affiliations_by_city), dict(universities_by_city)

def main():
    # Create mappers directory
    create_directories()
    
    # Read and update affiliations data
    print("Reading affiliations data...")
    project_root = get_project_root()
    affiliations_df = pd.read_csv(project_root / "data/transformed/affiliations.csv")
    affiliations_df = update_affiliation(affiliations_df)
    
    # Prepare mappers
    print("Preparing affiliation and university mappers...")
    affiliations_by_city, universities_by_city = prepare_affiliation_mappers(affiliations_df)
    
    # Save mappers to JSON files
    print("Saving mappers to files...")
    with open(project_root / "mappers/affiliations_by_city.json", 'w', encoding='utf-8') as f:
        json.dump(affiliations_by_city, f, ensure_ascii=False, indent=4)
    
    with open(project_root / "mappers/universities_by_city.json", 'w', encoding='utf-8') as f:
        json.dump(universities_by_city, f, ensure_ascii=False, indent=4)
    
    print("Mappers saved successfully!")

if __name__ == "__main__":
    main()
