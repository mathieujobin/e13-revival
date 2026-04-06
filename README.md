# E13 Revival - KWin Window Decoration Engine

A window decoration engine for KWin that faithfully replicates the E13 (Enlightenment 13) look and feel. This decoration provides a classic, elegant window frame style with support for theme switching, customizable borders, flexible button layouts, and dynamic rendering.

## Features

- **E13 Classic Style**: Faithful recreation of the E13 window decoration aesthetic
- **Theme Support**: Fully customizable colors and dimensions via configuration files
- **Dynamic Rendering**: Responsive to window state changes (active/inactive, maximized, shaded)
- **Flexible Button Layouts**: Configurable button positions and types
- **Border Styles**: Multiple border sizes from tiny to oversized
- **KWin Integration**: Tight integration with KDE's KWin window manager API
- **Modern Implementation**: Built with KDecoration2 framework and Qt5

## Requirements

- CMake 3.16 or later
- Qt5 (Core, Gui, Widgets)
- KDE Frameworks 5 (KConfig, CoreAddons, GuiAddons, I18n)
- KDecoration2
- KWin 5.x or later

## Building

```bash
mkdir build
cd build
cmake ..
make
```

## Installation

```bash
sudo make install
```

After installation, restart KWin or log out and back in:

```bash
kwin_x11 --replace &  # For X11
# or
kwin_wayland --replace &  # For Wayland
```

## Activation

1. Open System Settings
2. Navigate to "Appearance" → "Window Decorations"
3. Select "E13 Revival" from the list
4. Click "Apply"

Alternatively, use the command line:

```bash
kwriteconfig5 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kdecoration2.e13
qdbus org.kde.KWin /KWin reconfigure
```

## Theme Customization

The decoration can be customized by editing the configuration file:

```
~/.config/e13decorationrc
```

Or system-wide:

```
/etc/xdg/e13decorationrc
```

### Configuration Options

#### General Settings
- `BorderWidth`: Width of window borders (default: 4)
- `TitleBarHeight`: Height of the title bar (default: 24)
- `EnableShadows`: Enable window shadows (default: true)

#### Colors
- `ActiveFrameColor`: Frame color for active windows
- `ActiveTitleBarColor`: Title bar color for active windows
- `ActiveTextColor`: Text color for active windows
- `InactiveFrameColor`: Frame color for inactive windows
- `InactiveTitleBarColor`: Title bar color for inactive windows
- `InactiveTextColor`: Text color for inactive windows
- `ButtonHoverColor`: Button color on mouse hover
- `ButtonPressColor`: Button color when pressed
- `CloseButtonColor`: Color for the close button icon

#### Buttons
- `ButtonSize`: Size of window buttons (default: 24)
- `ButtonSpacing`: Space between buttons (default: 2)
- `LeftButtons`: Button layout for left side (default: M for menu)
- `RightButtons`: Button layout for right side (default: IAX for minimize, maximize, close)

Button codes:
- `M` = Menu (application icon)
- `I` = Minimize
- `A` = Maximize
- `X` = Close
- `K` = Keep Above
- `B` = Keep Below
- `S` = Shade
- `D` = On All Desktops

#### Advanced
- `Antialiasing`: Enable smooth rendering (default: true)
- `TitleFontSize`: Font size for window titles (default: 10)
- `TitleBold`: Make title text bold (default: false)

### Example Custom Theme

Create or edit `~/.config/e13decorationrc`:

```ini
[General]
BorderWidth=6
TitleBarHeight=28
EnableShadows=true

[Colors]
ActiveFrameColor=#1a1a1f
ActiveTitleBarColor=#2a2a35
ActiveTextColor=#e0e0e0
InactiveFrameColor=#2a2a2f
InactiveTitleBarColor=#3a3a45
InactiveTextColor=#808085

[Buttons]
ButtonSize=26
LeftButtons=M
RightButtons=KIAX
```

After editing, reload the decoration:

```bash
qdbus org.kde.KWin /KWin reconfigure
```

## Button Layout Customization

You can create different button layouts for various workflows:

**Minimal** (macOS-style):
```ini
LeftButtons=XIR
RightButtons=
```

**Classic E13**:
```ini
LeftButtons=M
RightButtons=IAX
```

**Full Featured**:
```ini
LeftButtons=MS
RightButtons=DKBIAX
```

## Development

### Project Structure

```
e13-revival/
├── CMakeLists.txt              # Main build configuration
├── src/                        # Source code
│   ├── CMakeLists.txt         # Source build config
│   ├── plugin.h/cpp           # KWin plugin interface
│   ├── decoration.h/cpp       # Main decoration class
│   └── button.h/cpp           # Window button rendering
├── decoration/                 # Metadata
│   └── metadata.json          # Plugin metadata
└── theme/                      # Theme files
    └── e13decorationrc        # Default theme configuration
```

### Architecture

The decoration engine consists of three main components:

1. **Plugin** (`plugin.h/cpp`): Implements the KDecoration2::DecorationFactory interface and serves as the entry point for KWin.

2. **Decoration** (`decoration.h/cpp`): Main decoration class that handles:
   - Border and title bar rendering
   - Window caption display
   - Theme loading and application
   - Dynamic updates based on window state
   - Button group management

3. **Button** (`button.h/cpp`): Individual window button implementation with:
   - Icon rendering for different button types
   - Hover and press states
   - E13-style visual design

## Troubleshooting

### Decoration not appearing in System Settings

Make sure the plugin is installed in the correct location:

```bash
find /usr -name "e13decoration.so" 2>/dev/null
```

Check that metadata is installed:

```bash
find /usr -name "metadata.json" | grep e13
```

### KWin crashes after installation

Check KWin logs:

```bash
journalctl -xe | grep kwin
```

Try running KWin with debug output:

```bash
QT_LOGGING_RULES="*decoration*=true" kwin_x11 --replace
```

### Theme changes not taking effect

Force KWin to reconfigure:

```bash
qdbus org.kde.KWin /KWin reconfigure
```

Or restart KWin completely:

```bash
kquitapp5 kwin_x11 && kwin_x11 &
# For Wayland:
kquitapp5 kwin_wayland && kwin_wayland &
```

### Building issues

If you get CMake errors about missing packages, install development packages:

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

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Credits

E13 Revival Project - Recreating the classic Enlightenment 13 experience for modern KDE environments.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

## Acknowledgments

- Original Enlightenment 13 (E13) window manager by Carsten "Rasterman" Haitzler
- KDE development team for the KDecoration2 framework
- KWin development team for the excellent window manager
