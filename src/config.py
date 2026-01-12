import yaml
import os

# Default configuration
DEFAULT_CONFIG = {
    "book": {
        "title": None, # Defaults to source directory name if None
        "subtitle": "",
        "author": "Anonymous"
    },
    "build": {
        "source_dir": "dist",
        "output_file": "book.pdf",
        "pdf_engine": "xelatex",
        "artifacts_dir": "build_artifacts"
    },
    "style": {
        "template": "eisvogel.latex",
        "mainfont": "LMRoman10-Regular",
        "sansfont": "Arial",
        "monofont": "LMMono10-Regular",
        "link_color": "07455c",
        "url_color": "07455c",
        "chapter_title_top_margin": "0pt",
        "chapter_title_bottom_margin": "20pt"
    },
    "mermaid": {
        "default_height": "11cm",
        "default_width": None,
        "scale": 3.0
    },
    "images": {
        "max_width": None, # Max width for images (scales down if larger)
        "max_height": "0.7\\linewidth", # Max height (if set, overrides width constraint)
        "keep_aspect_ratio": True
    },
    "tables": {
        "row_colors": True,
        "odd_color": "white",
        "even_color": "RoyalBlue!20",
        "stretch": 1.2
    },
    "resources": {
        "dir": "resources",
        "images_dir": "images"
    }
}

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load configuration from a YAML file, falling back to defaults.
    """
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(config_path):
        _merge_file_config(config, config_path)
    else:
        print(f"Config file {config_path} not found. Using defaults.")
    
    _apply_env_vars(config)
    _apply_fallbacks(config)
    
    return config

def _merge_file_config(config: dict, config_path: str) -> None:
    """Merges user config file into current config."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            
        for key, value in user_config.items():
            if key in config and isinstance(config[key], dict) and isinstance(value, dict):
                config[key].update(value)
            else:
                config[key] = value
        print(f"Loaded configuration from {config_path}")
    except Exception as e:
        print(f"Error loading config: {e}. Using defaults.")

def _apply_env_vars(config: dict) -> None:
    """Overrides config with environment variables."""
    if os.getenv("BOOK_TITLE"):
        config['book']['title'] = os.getenv("BOOK_TITLE")

    if os.getenv("BOOK_SUBTITLE"):
        config['book']['subtitle'] = os.getenv("BOOK_SUBTITLE")

    if os.getenv("BOOK_AUTHOR"):
        config['book']['author'] = os.getenv("BOOK_AUTHOR")
    
    if os.getenv("SOURCE_DIR"):
        config['build']['source_dir'] = os.getenv("SOURCE_DIR")
        
    if os.getenv("OUTPUT_FILE"):
        config['build']['output_file'] = os.getenv("OUTPUT_FILE")

def _apply_fallbacks(config: dict) -> None:
    """Applies dynamic defaults based on other values."""
    if not config['book'].get('title'):
        source_dir = config['build'].get('source_dir')
        if source_dir:
             abs_source = os.path.abspath(source_dir)
             config['book']['title'] = os.path.basename(abs_source)

    return config

# Global config instance to be used across modules
CONFIG = load_config()
