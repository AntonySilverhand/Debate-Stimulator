import json
import os
from pathlib import Path

def load_config():
    """
    Load configuration from config.json file
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = Path(__file__).resolve().parent / "config.json"
    with open(config_path, "r") as f:
        return json.load(f)

def get_config(key, default=None):
    """
    Get configuration value from config.json
    
    Args:
        key (str): Configuration key
        default: Default value if key not found
        
    Returns:
        Value from config or default if not found
    """
    config = load_config()
    return config.get(key, default)