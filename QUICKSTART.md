# Quick Start Guide - E13 Revival Window Decoration

Get up and running with E13 Revival in minutes!

## Prerequisites

You need a KDE Plasma desktop environment with:
- KDE Plasma 5.x or later
- KWin window manager
- Development tools and libraries (see below)

## Installation (3 Steps)

### Step 1: Install Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install cmake extra-cmake-modules qtbase5-dev \
    libkf5config-dev libkf5coreaddons-dev libkf5guiaddons-dev \
    libkf5i18n-dev kdecoration-dev kwin-dev
```

**Fedora:**
```bash
sudo dnf install cmake extra-cmake-modules qt5-qtbase-devel \
    kf5-kconfig-devel kf5-kcoreaddons-devel kf5-kguiaddons-devel \
    kf5-ki18n-devel kdecoration-devel kwin-devel
```

**Arch Linux:**
```bash
sudo pacman -S cmake extra-cmake-modules qt5-base \
    kconfig kcoreaddons kguiaddons ki18n kdecoration kwin
```

### Step 2: Build

```bash
./build.sh
```

The build script will:
- Check for all required dependencies
- Configure the build with CMake
- Compile the decoration
- Report success or errors

### Step 3: Install

```bash
cd build
sudo make install
```

## Activation (Choose One)

### Option 1: GUI (Recommended)
1. Open **System Settings**
2. Go to **Appearance** → **Window Decorations**
3. Select **E13 Revival** from the list
4. Click **Apply**

### Option 2: Command Line
```bash
kwriteconfig5 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kdecoration2.e13
qdbus org.kde.KWin /KWin reconfigure
```

## Verify Installation

You should now see E13-style window decorations on all windows!

Check for:
- Dark gray title bars
- Clean, minimal borders
- Window buttons on the right
- Application icon on the left

## Customization

### Change Theme

Copy one of the included themes:

```bash
# Light theme
cp theme/light.e13decorationrc ~/.config/e13decorationrc
qdbus org.kde.KWin /KWin reconfigure

# Dark blue theme
cp theme/dark-blue.e13decorationrc ~/.config/e13decorationrc
qdbus org.kde.KWin /KWin reconfigure

# Minimal theme
cp theme/minimal.e13decorationrc ~/.config/e13decorationrc
qdbus org.kde.KWin /KWin reconfigure
```

### Edit Theme

```bash
# Edit your theme
nano ~/.config/e13decorationrc

# Apply changes
qdbus org.kde.KWin /KWin reconfigure
```

See `theme/README.md` for full customization options.

## Troubleshooting

### Decoration Not Showing

**Check installation:**
```bash
find /usr -name "e13decoration.so" 2>/dev/null
```

**Restart KWin:**
```bash
kquitapp5 kwin_x11 && kwin_x11 &
```

### Build Fails

**Missing dependencies?**
Run the build script - it will tell you what's missing:
```bash
./build.sh
```

**CMake errors?**
```bash
rm -rf build
./build.sh
```

### Theme Not Loading

**Check file location:**
```bash
ls -la ~/.config/e13decorationrc
```

**Check file syntax:**
```bash
cat ~/.config/e13decorationrc
```

Look for typos in section headers `[General]`, `[Colors]`, etc.

### Get Help

**Check logs:**
```bash
journalctl -xe | grep kwin | tail -20
```

**Report issues:**
Open an issue on GitHub with:
- Your Linux distribution and version
- KDE Plasma version
- Error messages from build or logs

## Next Steps

### Explore Features
- **Multiple border sizes**: Change in System Settings
- **Button layouts**: Edit `LeftButtons` and `RightButtons` in config
- **Custom colors**: Modify color values in theme file
- **Font customization**: Adjust `TitleFontSize` and `TitleBold`

### Read Documentation
- **README.md**: Complete user manual
- **DESIGN.md**: Visual design specification
- **FEATURES.md**: Complete feature list
- **theme/README.md**: Theme creation guide

### Contribute
- **CONTRIBUTING.md**: Developer guide
- Report bugs on GitHub
- Submit theme ideas
- Contribute code improvements

## Common Customizations

### Make Borders Thicker
```ini
[General]
BorderWidth=8
```

### Change Close Button Color
```ini
[Colors]
CloseButtonColor=#ff0000  # Bright red
```

### Move All Buttons to Left
```ini
[Buttons]
LeftButtons=MIAX
RightButtons=
```

### Use Bold Title Text
```ini
[Advanced]
TitleBold=true
```

## Uninstallation

To remove E13 decoration:

```bash
# Switch to different decoration first
kwriteconfig5 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kdecoration2.aurorae

# Reload KWin
qdbus org.kde.KWin /KWin reconfigure

# Remove files
sudo find /usr -name "*e13decoration*" -delete
sudo find /usr -name "metadata.json" -path "*/e13*" -delete
```

## Resources

- **Project Repository**: https://github.com/mathieujobin/e13-revival
- **Issue Tracker**: GitHub Issues
- **Documentation**: README.md, DESIGN.md, FEATURES.md

## Summary

That's it! You now have a beautiful E13-style window decoration running on your KDE Plasma desktop. Customize it to your liking and enjoy the classic E13 aesthetic!

---

**Time to Install**: ~5-10 minutes
**Difficulty**: Beginner-friendly
**Support**: Community-driven

Enjoy your E13 Revival experience! 🎉
