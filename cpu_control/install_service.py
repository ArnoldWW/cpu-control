#!/usr/bin/env python3
import sys
import os
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cpu_control.config import save_config

SERVICE_CONTENT = """[Unit]
Description=CPU Frequency Control
After=multi-user.target

[Service]
Type=oneshot
ExecStart={python_path} {startup_path}
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""

if __name__ == "__main__":
    min_freq = int(sys.argv[1])
    max_freq = int(sys.argv[2])
    governor = sys.argv[3]
    
    # Save configuration
    save_config(min_freq, max_freq, governor)
    print(f"Configuration saved: min={min_freq}, max={max_freq}, governor={governor}")
    
    # Create service file
    startup_path = os.path.join(os.path.dirname(__file__), "startup.py")
    python_path = sys.executable
    
    service_content = SERVICE_CONTENT.format(
        python_path=python_path,
        startup_path=startup_path
    )
    
    service_file = "/etc/systemd/system/cpu-control.service"
    
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print("Service file created")
    
    # Reload systemd
    subprocess.run(["systemctl", "daemon-reload"])
    
    # Enable service
    subprocess.run(["systemctl", "enable", "cpu-control.service"])
    
    print("Service enabled successfully")