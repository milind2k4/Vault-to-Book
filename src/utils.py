import re
import os

def clean_title(filename: str) -> str:
    """
    Extracts a clean title from the filename.
    Removes leading numbers (01, 01_, 01 -, etc.) and extension.
    """
    base = os.path.splitext(filename)[0]
    # Remove leading numbering patterns like "01 ", "01_", "01-", "1. "
    cleaned = re.sub(r'^[\d\s\.\-_]+', '', base)
    return cleaned.strip()

def slugify(text: str) -> str:
    """
    Creates a simple ID from text.
    """
    return re.sub(r'[^a-zA-Z0-9-]', '', text.lower().replace(' ', '-'))

def ensure_dir(path: str) -> None:
    """
    Ensures that a directory exists.
    """
    if not os.path.exists(path):
        os.makedirs(path)
