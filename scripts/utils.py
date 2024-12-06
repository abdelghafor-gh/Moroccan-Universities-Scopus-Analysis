from pathlib import Path
import os

def get_project_root():
    """Get the project root directory from the script location"""
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    return current_dir.parent

def create_directories():
    """Create all necessary directories for the project if they don't exist"""
    project_root = get_project_root()
    
    # List of directories to create
    directories = [
        # Data directories
        project_root / "data/transformed",  # Transformed source files
        project_root / "data/final",        # Combined data
        project_root / "data/fact",         # Fact tables
        project_root / "data/dimensions",   # Dimension tables
        
        # Support directories
        project_root / "mappers",           # Mapping files
        # project_root / "logs"               # Log files (for future use)
    ]
    
    # Create each directory if it doesn't exist
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        
    print(" Project directories created successfully")
