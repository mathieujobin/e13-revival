#!/bin/bash
# E13 Revival Window Decoration - Build and Install Script

set -e

echo "========================================"
echo "E13 Revival Window Decoration Builder"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root for installation
if [ "$EUID" -eq 0 ] && [ "$1" != "--install-only" ]; then
  echo -e "${RED}Warning: Running as root. Build as regular user, then use 'sudo' for install only.${NC}"
  exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "Checking for required build tools..."
MISSING_TOOLS=0

if ! command_exists cmake; then
    echo -e "${RED}✗ CMake not found${NC}"
    MISSING_TOOLS=1
else
    echo -e "${GREEN}✓ CMake found${NC}"
fi

if ! command_exists make; then
    echo -e "${RED}✗ Make not found${NC}"
    MISSING_TOOLS=1
else
    echo -e "${GREEN}✓ Make found${NC}"
fi

if ! command_exists pkg-config; then
    echo -e "${RED}✗ pkg-config not found${NC}"
    MISSING_TOOLS=1
else
    echo -e "${GREEN}✓ pkg-config found${NC}"
fi

if [ $MISSING_TOOLS -eq 1 ]; then
    echo ""
    echo -e "${RED}Missing required build tools. Please install them first.${NC}"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install cmake make pkg-config"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install cmake make pkg-config"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S cmake make pkg-config"
    exit 1
fi

# Check for required libraries
echo ""
echo "Checking for required libraries..."
MISSING_LIBS=0

if ! pkg-config --exists Qt5Core; then
    echo -e "${RED}✗ Qt5 not found${NC}"
    MISSING_LIBS=1
else
    echo -e "${GREEN}✓ Qt5 found ($(pkg-config --modversion Qt5Core))${NC}"
fi

if ! pkg-config --exists KF5Config; then
    echo -e "${RED}✗ KDE Frameworks 5 not found${NC}"
    MISSING_LIBS=1
else
    echo -e "${GREEN}✓ KDE Frameworks 5 found ($(pkg-config --modversion KF5Config))${NC}"
fi

# KDecoration2 check (might not have pkg-config file)
if [ -f "/usr/include/KDecoration2/kdecoration2/decoration.h" ] || [ -f "/usr/local/include/KDecoration2/kdecoration2/decoration.h" ]; then
    echo -e "${GREEN}✓ KDecoration2 headers found${NC}"
else
    echo -e "${RED}✗ KDecoration2 not found${NC}"
    MISSING_LIBS=1
fi

if [ $MISSING_LIBS -eq 1 ]; then
    echo ""
    echo -e "${RED}Missing required libraries. Please install them first.${NC}"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install extra-cmake-modules qtbase5-dev \\"
    echo "      libkf5config-dev libkf5coreaddons-dev libkf5guiaddons-dev \\"
    echo "      libkf5i18n-dev kdecoration-dev kwin-dev"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install extra-cmake-modules qt5-qtbase-devel \\"
    echo "      kf5-kconfig-devel kf5-kcoreaddons-devel kf5-kguiaddons-devel \\"
    echo "      kf5-ki18n-devel kdecoration-devel kwin-devel"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S extra-cmake-modules qt5-base \\"
    echo "      kconfig kcoreaddons kguiaddons ki18n kdecoration kwin"
    exit 1
fi

# Create build directory
echo ""
echo "Setting up build directory..."
rm -rf build
mkdir build
cd build

# Configure
echo ""
echo "Configuring build with CMake..."
if ! cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release; then
    echo -e "${RED}Configuration failed!${NC}"
    exit 1
fi

# Build
echo ""
echo "Building..."
if ! make -j$(nproc); then
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Build completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To install, run:"
echo "  cd build && sudo make install"
echo ""
echo "After installation, activate the decoration:"
echo "  kwriteconfig5 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kdecoration2.e13"
echo "  qdbus org.kde.KWin /KWin reconfigure"
echo ""
echo "Or use System Settings > Appearance > Window Decorations"
