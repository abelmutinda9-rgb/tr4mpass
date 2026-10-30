
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKGROOT="$ROOT/build/package"
VERSION="${VERSION:-0.1.0}"
ARCH="all"
OUT="$ROOT/build/tr4mpass-desktop_${VERSION}_${ARCH}.deb"

rm -rf "$PKGROOT"
mkdir -p "$PKGROOT/DEBIAN"
mkdir -p "$PKGROOT/usr/share/tr4mpass-desktop"
mkdir -p "$PKGROOT/usr/bin"
mkdir -p "$PKGROOT/usr/share/applications"

install -m 0644 "$ROOT/desktop/app.py" \
  "$PKGROOT/usr/share/tr4mpass-desktop/app.py"

cat > "$PKGROOT/DEBIAN/control" <<CONTROL
Package: tr4mpass-desktop
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: tr4mpass desktop contributors
Depends: python3, python3-tk, usbutils, libimobiledevice-utils
Description: Desktop USB device diagnostics interface
 A graphical interface for USB device listing and
 available iOS device information commands.
CONTROL

cat > "$PKGROOT/usr/bin/tr4mpass-desktop" <<'LAUNCHER'
#!/bin/sh
exec /usr/bin/python3 /usr/share/tr4mpass-desktop/app.py "$@"
LAUNCHER
chmod 0755 "$PKGROOT/usr/bin/tr4mpass-desktop"

cat > "$PKGROOT/usr/share/applications/tr4mpass-desktop.desktop" <<'DESKTOP'
[Desktop Entry]
Name=tr4mpass Desktop
Comment=USB device diagnostics
Exec=tr4mpass-desktop
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;System;
DESKTOP
chmod 0644 "$PKGROOT/usr/share/applications/tr4mpass-desktop.desktop"

mkdir -p "$ROOT/build"
dpkg-deb --root-owner-group --build "$PKGROOT" "$OUT"

echo "Built package: $OUT"
