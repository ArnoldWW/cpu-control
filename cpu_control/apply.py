#!/usr/bin/env python3
import sys
import os

# Add parent directory to path to import cpu_control
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cpu_control.cpufreq import set_limits, set_governor

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: apply_helper.py <min_freq> <max_freq> <governor>")
        sys.exit(1)
    
    min_freq = int(sys.argv[1])
    max_freq = int(sys.argv[2])
    governor = sys.argv[3]
    
    try:
        set_limits(min_freq, max_freq)
        set_governor(governor)
        print(f"Applied: min={min_freq}, max={max_freq}, governor={governor}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)