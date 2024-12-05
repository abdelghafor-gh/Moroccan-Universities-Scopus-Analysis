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
        project_root / "data/transformed",
        project_root / "mappers"
    ]
    
    # Create each directory if it doesn't exist
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
