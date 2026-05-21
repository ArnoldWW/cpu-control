#!/usr/bin/env python3
import subprocess
import os
import sys

SERVICE_NAME = "cpu-control.service"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"

if __name__ == "__main__":
    try:
        subprocess.run(
            ["systemctl", "stop", SERVICE_NAME],
            check=True,
        )
        subprocess.run(
            ["systemctl", "disable", SERVICE_NAME], 
            check=True, 
        )
        
        if os.path.exists(SERVICE_PATH):
            os.remove(SERVICE_PATH)

        subprocess.run(
            ["systemctl", "daemon-reload"],
            check=True,
        )
        print("Systemd service removed successfully.")

    except Exception as e:
        print(f"Error removing systemd service: {e}")
        sys.exit(1)