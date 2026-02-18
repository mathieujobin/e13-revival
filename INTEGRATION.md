# Integration Guide

This guide explains how to integrate extracted E13 theme data into modern desktop environments and applications.

## Table of Contents

1. [KWin Window Decoration](#kwin-window-decoration)
2. [Icon Themes](#icon-themes)
3. [GTK/Qt Themes](#gtkqt-themes)
4. [Wallpapers](#wallpapers)
5. [Custom Applications](#custom-applications)

## Overview

After extracting a theme using the `extract_theme.py` tool, you'll have:

```
extracted_theme/
├── metadata.json              # Theme metadata and configuration
├── theme_info.json           # Parsed theme information
├── extraction_summary.json   # Extraction details
├── images/                   # Extracted images (PNG format)
│   ├── background.png
│   ├── border_*.png
│   └── ...
├── icons/                    # Icons (if present)
│   └── ...
└── styles/                   # Style configurations
    └── ...
```

## KWin Window Decoration

KWin (KDE Window Manager) can use extracted border and window decoration images.

### Structure

KWin decorations typically need:
- Title bar images (active/inactive states)
- Border images (top, bottom, left, right)
- Button images (close, minimize, maximize)

### Steps

1. **Extract the theme**:
```bash
python3 tools/extract_theme.py -i theme.db -o ./kwin_theme/
```

2. **Organize images** for KWin structure:
```bash
mkdir -p ~/.local/share/kwin/decorations/e13-theme/
cp ./kwin_theme/images/border_top*.png ~/.local/share/kwin/decorations/e13-theme/
cp ./kwin_theme/images/border_bottom*.png ~/.local/share/kwin/decorations/e13-theme/
# ... copy other relevant images
```

3. **Create KWin decoration config**:
```ini
# ~/.local/share/kwin/decorations/e13-theme/e13-themerc
[General]
Name=E13 Revival Theme
Description=Extracted from Enlightenment 0.13
Version=1.0

[Windeco]
TitleBarHeight=24
BorderLeft=2
BorderRight=2
BorderBottom=2

[Images]
ActiveTitleBar=border_top_active.png
InactiveTitleBar=border_top_inactive.png
BorderLeft=border_left.png
BorderRight=border_right.png
BorderBottom=border_bottom.png
```

4. **Apply in KWin**:
   - System Settings → Appearance → Window Decorations
   - Select your imported E13 theme

## Icon Themes

Convert extracted icons to freedesktop.org icon theme format.

### Structure

```
~/.local/share/icons/e13-theme/
├── index.theme
├── 16x16/
│   ├── apps/
│   ├── actions/
│   └── ...
├── 22x22/
│   └── ...
├── 32x32/
│   └── ...
└── scalable/
    └── ...
```

### Steps

1. **Extract icons**:
```bash
python3 tools/extract_theme.py -i theme.db -o ./icons_extracted/
```

2. **Create icon theme structure**:
```bash
mkdir -p ~/.local/share/icons/e13-theme/{16x16,22x22,32x32,48x48}/apps
```

3. **Copy and organize icons**:
```bash
# Organize by size (resize if needed with ImageMagick/Pillow)
convert icons_extracted/images/icon_app.png -resize 16x16 \
    ~/.local/share/icons/e13-theme/16x16/apps/application.png
```

4. **Create index.theme**:
```ini
[Icon Theme]
Name=E13 Revival Icons
Comment=Icons extracted from Enlightenment 0.13 theme
Inherits=hicolor
Directories=16x16/apps,22x22/apps,32x32/apps,48x48/apps

[16x16/apps]
Size=16
Context=Applications
Type=Fixed

[22x22/apps]
Size=22
Context=Applications
Type=Fixed

[32x32/apps]
Size=32
Context=Applications
Type=Fixed

[48x48/apps]
Size=48
Context=Applications
Type=Fixed
```

5. **Update icon cache**:
```bash
gtk-update-icon-cache ~/.local/share/icons/e13-theme/
```

## GTK/Qt Themes

Extract color schemes and styling information.

### For GTK

1. **Extract theme**:
```bash
python3 tools/extract_theme.py -i theme.db -o ./gtk_theme/
```

2. **Analyze metadata.json** for color schemes:
```bash
cat gtk_theme/metadata.json | grep -i color
```

3. **Create GTK CSS** from extracted data:
```css
/* ~/.config/gtk-3.0/gtk.css or theme file */
* {
    /* Use colors from metadata.json */
    background-color: #xxxxxx;
    color: #yyyyyy;
}

button {
    border-image: url("border_button.png");
}
```

### For Qt

1. **Extract theme and analyze**:
```bash
python3 tools/extract_theme.py -i theme.db -o ./qt_theme/
cat qt_theme/theme_info.json
```

2. **Create Qt stylesheet** (.qss):
```css
/* Use extracted colors and images */
QWidget {
    background-color: #xxxxxx;
}

QPushButton {
    border-image: url(border_button.png);
}
```

## Wallpapers

Use extracted background images as wallpapers.

### Steps

1. **Extract backgrounds**:
```bash
python3 tools/extract_theme.py -i theme.db -o ./wallpapers/
```

2. **Find background images**:
```bash
ls wallpapers/images/ | grep -i "background\|wallpaper\|bg"
```

3. **Copy to wallpaper directory**:
```bash
mkdir -p ~/.local/share/wallpapers/e13-revival/
cp wallpapers/images/background*.png ~/.local/share/wallpapers/e13-revival/
```

4. **Set as wallpaper**:
   - KDE: System Settings → Appearance → Wallpaper
   - GNOME: Settings → Background
   - XFCE: Settings → Desktop → Background
   - Or use: `feh --bg-scale ~/.local/share/wallpapers/e13-revival/background.png`

## Custom Applications

Use the Python API to programmatically access theme data.

### Example: Load Theme in Python

```python
from pathlib import Path
import sys
sys.path.append('tools')

from imlib_db_parser import parse_db_file

# Parse theme
theme = parse_db_file(Path('theme.db'))

# Get all image keys
images = theme.get_image_keys()
print(f"Found {len(images)} images")

# Extract specific image
bg_data = theme.get_entry('background.png')
if bg_data:
    with open('my_background.png', 'wb') as f:
        f.write(bg_data)

# Get metadata
text_keys = theme.get_text_keys()
for key in text_keys:
    text = theme.extract_text(key)
    print(f"{key}: {text}")
```

### Example: Theme Preview Application

```python
#!/usr/bin/env python3
"""
Simple theme preview application
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import sys
sys.path.append('tools')

from imlib_db_parser import parse_db_file

class ThemePreview:
    def __init__(self, db_path):
        self.theme = parse_db_file(db_path)
        self.root = tk.Tk()
        self.root.title("E13 Theme Preview")
        
        # Get theme info
        theme_name = self.theme.extract_text('theme/name') or 'Unknown Theme'
        ttk.Label(self.root, text=theme_name, font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Display images
        for img_key in self.theme.get_image_keys()[:5]:  # First 5 images
            img_data = self.theme.get_entry(img_key)
            img = Image.open(BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)
            
            label = ttk.Label(self.root, image=photo)
            label.image = photo  # Keep reference
            label.pack(pady=5)
            
            ttk.Label(self.root, text=img_key).pack()
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: theme_preview.py <theme.db>")
        sys.exit(1)
    
    preview = ThemePreview(sys.argv[1])
    preview.run()
```

## Batch Processing

Process multiple themes at once:

```bash
#!/bin/bash
# batch_extract.sh

for theme in /path/to/themes/*.db; do
    theme_name=$(basename "$theme" .db)
    echo "Extracting $theme_name..."
    python3 tools/extract_theme.py -i "$theme" -o "./extracted/$theme_name"
done
```

## Tips and Best Practices

1. **Image Formats**: The tool converts all extracted images to PNG for maximum compatibility
2. **Metadata**: Always check `metadata.json` and `theme_info.json` for theme-specific information
3. **Naming**: Original E13 key names are preserved in extracted filenames
4. **Colors**: Extract color information from metadata for consistent theming
5. **Scaling**: Some images may need to be scaled for modern high-DPI displays

## Troubleshooting

### Images not extracting
- Check if the DB file is a valid Imlib DB format
- Try verbose mode: `python3 tools/extract_theme.py -i theme.db -o output/ -v`

### Missing metadata
- Some themes may not have embedded metadata
- Check the extraction summary for details

### Incompatible formats
- The tool supports DB v1, v2, and generic extraction
- For unsupported formats, please open an issue

## Contributing

If you create integration tools or scripts, please contribute them back to the project!

## Resources

- [KWin Documentation](https://develop.kde.org/docs/plasma/)
- [Freedesktop Icon Theme Specification](https://specifications.freedesktop.org/icon-theme-spec/)
- [GTK Theming Guide](https://docs.gtk.org/gtk3/css-overview.html)
- [Qt Style Sheets](https://doc.qt.io/qt-5/stylesheet.html)
