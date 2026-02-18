#!/bin/bash
# E13 Revival Window Decoration - Installation Script
# Run this after building: cd build && sudo ./install.sh

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run with sudo: sudo ./install.sh"
  exit 1
fi

echo "Installing E13 Revival Window Decoration..."

# Install the plugin
make install

echo ""
echo "Installation complete!"
echo ""
echo "To activate the decoration, run as your user (not root):"
echo "  kwriteconfig5 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kdecoration2.e13"
echo "  qdbus org.kde.KWin /KWin reconfigure"
echo ""
echo "Or restart KWin:"
echo "  kquitapp5 kwin_x11 && kwin_x11 &"
echo ""
echo "You can also activate it through System Settings:"
echo "  System Settings > Appearance > Window Decorations > E13 Revival"
