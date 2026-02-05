#!/usr/bin/env python3
import subprocess
import os

service_name = "cpu-control.service"
service_path = f"/etc/systemd/system/{service_name}"

try:
    subprocess.run(["systemctl", "disable", service_name], check=True)
    if os.path.exists(service_path):
        os.remove(service_path)
    subprocess.run(["systemctl", "daemon-reload"], check=True)
    print("Systemd service removed successfully.")
except Exception as e:
    print(f"Failed to remove service: {e}")
    exit(1)