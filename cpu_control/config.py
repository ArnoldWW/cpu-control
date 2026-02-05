import json
import os

CONFIG_FILE = "/etc/cpu-control.conf"

def save_config(min_freq, max_freq, governor):
    """Save configuration to file (requires root)"""
    config = {
        "min_freq": min_freq,
        "max_freq": max_freq,
        "governor": governor
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    """Load configuration from file"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return None