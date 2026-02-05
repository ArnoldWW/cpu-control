#!/bin/bash

VERSION="1.0"
PACKAGE="cpu-control"
BUILD_DIR="${PACKAGE}-${VERSION}"

# Clean previous build
rm -rf "$BUILD_DIR" "${PACKAGE}_${VERSION}_all.deb"

# Create directory structure
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/local/bin"
mkdir -p "$BUILD_DIR/usr/local/lib/python3/dist-packages/cpu_control"
mkdir -p "$BUILD_DIR/usr/share/applications"

# Create control file
cat > "$BUILD_DIR/DEBIAN/control" << EOF
Package: $PACKAGE
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-tk, polkitd
Maintainer: Arnold Rodriguez
Description: CPU Frequency Control GUI
 A graphical interface to control CPU frequency scaling and governor.
 Allows saving configuration to apply on boot via systemd service.
EOF

# Copy Python module
cp -r cpu_control/* "$BUILD_DIR/usr/local/lib/python3/dist-packages/cpu_control/"

# Create executable script
cat > "$BUILD_DIR/usr/local/bin/cpu-control" << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/local/lib/python3/dist-packages')
from cpu_control.app import CpuApp

if __name__ == "__main__":
    app = CpuApp()
    app.mainloop()
EOF

chmod 755 "$BUILD_DIR/usr/local/bin/cpu-control"

# Create desktop file
cat > "$BUILD_DIR/usr/share/applications/cpu-control.desktop" << 'EOF'
[Desktop Entry]
Name=CPU Control
Comment=Control CPU frequency and governor
Exec=cpu-control
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Settings;
EOF

# Build package
dpkg-deb --build "$BUILD_DIR"
mv "${BUILD_DIR}.deb" "${PACKAGE}_${VERSION}_all.deb"

echo "Package built: ${PACKAGE}_${VERSION}_all.deb"
echo "Install with: sudo dpkg -i ${PACKAGE}_${VERSION}_all.deb or sudo apt install ./${PACKAGE}_${VERSION}_all.deb"