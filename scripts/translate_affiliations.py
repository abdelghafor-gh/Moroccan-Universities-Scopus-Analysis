import pandas as pd
from pathlib import Path
import os
from utils import get_project_root, create_directories

# Dictionary of French to English translations
AFFILIATION_TRANSLATIONS = {
    # Universities
    "Université Abdelmalek Essaadi": "Abdelmalek Essaadi University",
    "Université Cadi Ayyad": "Cadi Ayyad University",
    "Université Chouaib Doukkali": "Chouaib Doukkali University",
    "Université Hassan 1er": "Hassan 1st University",
    "Université Hassan II": "Hassan II University",
    "Université Ibn Tofail": "Ibn Tofail University",
    "Université Ibn Zohr": "Ibn Zohr University", 
    "Université Mohammed Premier": "Mohammed First University",
    "Université Mohammed V": "Mohammed V University",
    "Université Moulay Ismail": "Moulay Ismail University", 
    "Université Sidi Mohamed Ben Abdellah": "Sidi Mohamed Ben Abdellah University",
    "Université Sultan Moulay Slimane": "Sultan Moulay Slimane University",

    # Faculty Translations
    "Faculté Oussoul Eddine": "Faculty of Fundamentals of Religion",
    "Faculté des Sciences Juridiques, Economiques et Sociales": "Faculty of Legal, Economic and Social Sciences",
    "Faculté des Sciences Juridiques et Politiques": "Faculty of Juridical and Political Sciences",
    "Faculté des Lettres et des Sciences Humaines": "Faculty of Letters and Humanities",
    "Faculté des Lettres et des Sciences Humaines Aïn Chock": "Faculty of Letters and Humanities Aïn Chock",
    "Faculté des Lettres et des Sciences Humaines Ben M'Sick": "Faculty of Letters and Humanities Ben M'Sick",
    "Faculté des Lettres et des Sciences Humaines Dhar El Mahraz": "Faculty of Letters and Humanities Dhar El Mahraz",
    "Faculté des Lettres et des Sciences Humaines Sais": "Faculty of Letters and Humanities Sais",
    "Faculté de la Langue Arabe": "Faculty of Arabic Language",
    "Faculté des Sciences": "Faculty of Sciences",
    "Faculté des Sciences Aïn Chock": "Faculty of Sciences Aïn Chock",
    "Faculté des Sciences Ben M'Sick": "Faculty of Sciences Ben M'Sick",
    "Faculté des Sciences Semlalia": "Faculty of Sciences Semlalia",
    "Faculté des Sciences Dhar El Mahraz": "Faculty of Sciences Dhar El Mahraz",
    "Faculté Polydisciplinaire": "Polydisciplinary Faculty",
    "Faculté des Sciences et Techniques": "Faculty of Sciences and Techniques",
    "Faculté des Sciences et Techniques Guéliz": "Faculty of Sciences and Techniques Guéliz",
    "Faculté des Sciences et Techniques Sais": "Faculty of Sciences and Techniques Sais",
    "Faculté de Médecine et Pharmacie": "Faculty of Medicine and Pharmacy",
    "Faculté de Médecine et de Pharmacie": "Faculty of Medicine and Pharmacy",
    "Faculté de Médecine Dentaire": "Faculty of Dental Medicine",
    "Faculté de Médecine, de Pharmacie et de Médecine Dentaire": "Faculty of Dental Medicine",
    "Faculté d'Economie et de Gestion": "Faculty of Economics and Management",
    "Faculté des Langues, Arts et Science humaines": "Faculty of Languages, Arts and Human Sciences",
    "Faculté des Sciences Appliquées": "Faculty of Applied Sciences",
    "Faculté des Sciences Juridiques, Economiques et Sociales Agdal": "Faculty of Legal, Economic and Social Sciences of Agdal",
    "Faculté des Sciences Juridiques, Economiques et Sociales Aïn Chock": "Faculty of Legal, Economic and Social Sciences of Aïn Chock",
    "Faculté des Sciences Juridiques, Economiques et Sociales Aïn Sebaa": "Faculty of Legal, Economic and Social Sciences of Aïn Sebaa",
    "Faculté des Sciences Juridiques, Economiques et Sociales Souissit": "Faculty of Legal, Economic and Social Sciences of Souissit",
    "Facultés des Langues, des Lettres et des Arts": "Faculty of Languages, Letters and Arts",
    "Faculté des Sciences Humaines et Sociale": "Faculty of Human and Social Sciences", 
    "Faculté Chariâa": "Faculty of Islamic Law (Sharia)",
    "Faculté des Sciences de l'Education": "Faculty of Educational Sciences",

    # School Translations
    "Ecole Nationale des Sciences Appliquées": "National School of Applied Sciences", 
    "Ecole Nationale Supérieure de l'Intelligence Artificielle et Sciences des Données": "National Higher School of Artificial Intelligence and Data Sciences",
    "Ecole Nationale Supérieure de l'Intelligence Artificielle et du Digital": "National Higher School of Artificial Intelligence and Digital Sciences",
    "Ecole Nationale de Commerce et de Gestion": "National School of Commerce and Management", 
    "Ecole Supérieure de l'Education et de la Formation": "Higher School of Education and Training",
    "Ecole Supérieure de Technologie": "Higher School of Technology", 
    "Ecole Nationale Supérieure de Chimie": "Natinal Higher School of Chemistry", 
    "Ecole Nationale Supérieure d'Electricité et de Mécanique": "National Higher School of Electricity and Mechanics", 
    "Ecole Nationale Supérieure des Arts et Métiers": "National Higher School of Arts and Crafts", 
    "Ecole Nationale Supérieure d'Art et Design": "National Higher School of Art and Design",
    "Ecole Normale Supérieure": "Higher Normal School", 
    "Ecole Mohammadia d'Ingénieurs": "Mohammadia Engineering School",
    "Ecole Nationale Supérieure d'Informatique et d'Analyse des Systèmes": "National Higher School of Computer Science and Systems Analysis", 
    "Ecole Normale Supérieure de l'Enseignement Technique": "Higher Normal School of Technical Education",
    "Ecole Supérieure Roi Fahd de Traduction": "King Fahd Higher School of Translation",

    # Institute Translations
    "Institut Supérieur des Sciences de la Santé": "Higher Institute of Health Sciences", 
    "Institut des Sciences du Sport": "Institute of Sports Sciences", 
    "Institut des Métiers du Sport": "Institute of Sports Professions",
    "Institut Scientifique": "Scientific Institute", 
    "Institut d'Etudes et de Recherches pour l'Arabisation": "Institute of Studies and Research for Arabization", 
    "Institut Universitaire des Etudes Africaines, Euro-méditerranéennes et Ibéro-américaines": "University Institute of African, Euro-Mediterranean and Ibero-American Studies"
}

def translate_affiliation(affiliation):
    """
    Translate a French affiliation to its English equivalent.
    
    Args:
        affiliation (str): French affiliation name
    Returns:
        str: English translation or original name if no translation found
    """
    return AFFILIATION_TRANSLATIONS.get(affiliation.strip(), affiliation)

def main():
    # Create necessary directories
    create_directories()
    project_root = get_project_root()
    
    # Read the affiliations data
    print("Reading affiliations data...")
    input_path = project_root / "data/raw/Universities-Affiliations/Moroccan-Affiliations.csv"
    affiliations_df = pd.read_csv(input_path)
    
    # Clean and translate affiliations
    print("Translating affiliations...")
    affiliations_df['Affiliation'] = affiliations_df['Affiliation'].apply(lambda aff: aff.strip())
    affiliations_df['Affiliation En Name'] = affiliations_df['Affiliation'].apply(translate_affiliation)
    
    # Save the translated data
    print("Saving translated data...")
    output_path = project_root / "data/transformed/affiliations.csv"
    affiliations_df.to_csv(output_path, index=False)
    
    print(f"Translations saved to {output_path}")

if __name__ == "__main__":
    main()
