# CPU Control

Personal GUI application to adjust minimum/maximum CPU frequency and governor on
Linux. Tested on Debian 13 xfce and Xubuntu.

![preview](preview/preview.png)

## Requirements

- Python 3
- tkinter
- polkitd (pkexec)
- Permissions to write to `/sys/devices/system/cpu`

## Usage in development

```bash
python3 -m cpu_control.app
```

# Install

Run `./build-deb.sh` and install the generated .deb file.

## Features

- Adjust minimum and maximum frequency
- Select governor
- Save configuration and create systemd service
