# E13 Decoration Themes

This directory contains theme configuration files for the E13 Revival window decoration.

## Available Themes

### Default Theme (`e13decorationrc`)
The classic E13 style with dark gray tones and moderate borders.

**Characteristics:**
- Border width: 4px
- Title bar height: 24px
- Dark gray color scheme
- Standard button size

**Best for:** General use, modern dark themes

### Dark Blue Theme (`dark-blue.e13decorationrc`)
A sophisticated dark theme with blue tinting.

**Characteristics:**
- Border width: 4px
- Title bar height: 24px
- Deep blue color scheme
- Comfortable for extended use

**Best for:** Night work, reducing eye strain

### Light Theme (`light.e13decorationrc`)
A clean, bright theme for light desktop environments.

**Characteristics:**
- Border width: 3px
- Title bar height: 26px
- Light gray color scheme
- High contrast text

**Best for:** Daytime use, light Plasma themes

### Minimal Theme (`minimal.e13decorationrc`)
Ultra-clean with minimal visual elements.

**Characteristics:**
- Border width: 2px
- Title bar height: 22px
- Monochrome colors
- No shadows
- Smaller buttons

**Best for:** Maximizing screen space, tiling workflows

### Classic Green Theme (`classic-green.e13decorationrc`)
Nostalgic theme inspired by original E13's green aesthetic.

**Characteristics:**
- Border width: 5px
- Title bar height: 26px
- Green-tinted colors
- Larger buttons
- Bold title text

**Best for:** E13 veterans, retro aesthetics

## Installing Themes

### System-wide Installation

Copy theme files to the system configuration directory:

```bash
sudo cp theme/*.e13decorationrc /etc/xdg/
```

### User Installation

Copy a theme file to your user config directory:

```bash
cp theme/dark-blue.e13decorationrc ~/.config/e13decorationrc
```

### Switching Themes

To switch to a different theme, simply copy the theme file over your active configuration:

```bash
# Switch to dark blue theme
cp theme/dark-blue.e13decorationrc ~/.config/e13decorationrc

# Reload KWin
qdbus org.kde.KWin /KWin reconfigure
```

Or rename the configuration:

```bash
# Keep original
mv ~/.config/e13decorationrc ~/.config/e13decorationrc.backup

# Activate new theme
cp theme/light.e13decorationrc ~/.config/e13decorationrc

# Reload KWin
qdbus org.kde.KWin /KWin reconfigure
```

## Creating Custom Themes

You can create your own themes by copying and modifying any of the provided theme files.

### Theme File Structure

```ini
[General]
BorderWidth=4              # Width of window borders (pixels)
TitleBarHeight=24          # Height of title bar (pixels)
EnableShadows=true         # Enable/disable window shadows

[Colors]
# Active window (focused)
ActiveFrameColor=#28282d         # Border color
ActiveTitleBarColor=#32323a      # Title bar background
ActiveTextColor=#ffffff          # Title text color

# Inactive window (not focused)
InactiveFrameColor=#3c3c41       # Border color
InactiveTitleBarColor=#464649    # Title bar background
InactiveTextColor=#a0a0a5        # Title text color

# Button colors
ButtonHoverColor=#464649         # Button background on hover
ButtonPressColor=#1e1e23         # Button background when clicked
CloseButtonColor=#dc5050         # Close button icon color

[Buttons]
ButtonSize=24              # Button dimensions (pixels)
ButtonSpacing=2            # Space between buttons (pixels)
LeftButtons=M              # Left side button layout
RightButtons=IAX           # Right side button layout

[Advanced]
Antialiasing=true          # Smooth rendering
TitleFontSize=10           # Title text size (points)
TitleBold=false            # Bold title text
```

### Button Layout Codes

- `M` = Menu (application icon)
- `I` = Minimize
- `A` = Maximize/Restore
- `X` = Close
- `K` = Keep Above
- `B` = Keep Below
- `S` = Shade/Unshade
- `D` = On All Desktops

### Color Format

Colors can be specified in several formats:

```ini
ActiveFrameColor=#28282d       # Hex RGB
ActiveFrameColor=#28282dff     # Hex RGBA (with alpha)
ActiveFrameColor=40,40,45      # Decimal RGB
```

### Tips for Custom Themes

1. **Contrast:** Ensure good contrast between text and background
2. **Consistency:** Keep active/inactive colors related but distinguishable
3. **Testing:** Test with both light and dark Plasma themes
4. **Sizing:** Balance border size with screen real estate
5. **Harmony:** Match colors with your Plasma color scheme

### Example: Creating a Purple Theme

```ini
[General]
BorderWidth=4
TitleBarHeight=24
EnableShadows=true

[Colors]
ActiveFrameColor=#2a1a32
ActiveTitleBarColor=#3a2442
ActiveTextColor=#f0d8ff

InactiveFrameColor=#3a2a42
InactiveTitleBarColor=#4a3452
InactiveTextColor=#a080b0

ButtonHoverColor=#4a3452
ButtonPressColor=#2a1a32
CloseButtonColor=#e85080

[Buttons]
ButtonSize=24
ButtonSpacing=2
LeftButtons=M
RightButtons=IAX

[Advanced]
Antialiasing=true
TitleFontSize=10
TitleBold=false
```

Save as `theme/purple.e13decorationrc` and activate:

```bash
cp theme/purple.e13decorationrc ~/.config/e13decorationrc
qdbus org.kde.KWin /KWin reconfigure
```

## Troubleshooting

### Theme Not Loading

1. Check file permissions:
   ```bash
   chmod 644 ~/.config/e13decorationrc
   ```

2. Verify file syntax (look for missing brackets, etc.)

3. Check KWin logs:
   ```bash
   journalctl -xe | grep kwin
   ```

### Colors Not Appearing Correctly

- Ensure color values are valid hex codes (#RRGGBB)
- Check that alpha channel is specified correctly if used
- Verify no typos in color names

### Changes Not Taking Effect

Force KWin reload:

```bash
kquitapp5 kwin_x11 && kwin_x11 &
# For Wayland:
kquitapp5 kwin_wayland && kwin_wayland &
```

Or restart your session.

## Sharing Themes

If you create an interesting theme, consider contributing it:

1. Create a new theme file in the `theme/` directory
2. Add a description to this README
3. Submit a pull request

## Gallery

### Screenshots

You can find screenshots of each theme in the project wiki or documentation.

### Community Themes

Check the project issues/discussions for community-contributed themes!

---

For more information, see the main [README.md](../README.md).
