# CPU Control

GUI application to adjust minimum/maximum CPU frequency and governor on Linux.

## Requirements

- Python 3
- tkinter
- polkitd (pkexec)
- Permissions to write to `/sys/devices/system/cpu`

## Usage

```bash
python3 -m cpu_control.app
```

## Features

- Adjust minimum and maximum frequency
- Select governor
- Save configuration and create systemd service
