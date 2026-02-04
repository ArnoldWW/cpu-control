#!/usr/bin/env python3
import sys
import os
import json

CONFIG_FILE = "/etc/cpu-control.conf"

def load_config():
    """Load configuration from file"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return None

def set_cpu_frequencies(min_freq, max_freq):
    """Set CPU frequencies for all CPUs"""
    cpu_paths = []
    cpu_dir = "/sys/devices/system/cpu"
    
    for entry in os.listdir(cpu_dir):
        if entry.startswith("cpu") and entry[3:].isdigit():
            cpufreq_path = os.path.join(cpu_dir, entry, "cpufreq")
            if os.path.exists(cpufreq_path):
                cpu_paths.append(cpufreq_path)
    
    for cpu_path in cpu_paths:
        with open(os.path.join(cpu_path, "scaling_min_freq"), 'w') as f:
            f.write(str(min_freq))
        with open(os.path.join(cpu_path, "scaling_max_freq"), 'w') as f:
            f.write(str(max_freq))

def set_governor(governor):
    """Set governor for all CPUs"""
    cpu_dir = "/sys/devices/system/cpu"
    
    for entry in os.listdir(cpu_dir):
        if entry.startswith("cpu") and entry[3:].isdigit():
            cpufreq_path = os.path.join(cpu_dir, entry, "cpufreq")
            if os.path.exists(cpufreq_path):
                with open(os.path.join(cpufreq_path, "scaling_governor"), 'w') as f:
                    f.write(governor)

if __name__ == "__main__":
    config = load_config()
    if config:
        try:
            set_cpu_frequencies(config["min_freq"], config["max_freq"])
            set_governor(config["governor"])
            print("CPU configuration applied successfully")
        except Exception as e:
            print(f"Error applying configuration: {e}")
            sys.exit(1)
    else:
        print("No configuration file found")
        sys.exit(1)