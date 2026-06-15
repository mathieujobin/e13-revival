# Quick Start Guide

Get started with the E13 Revival theme extraction tool in 5 minutes.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mathieujobin/e13-revival.git
cd e13-revival
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! The tool is ready to use.

## Basic Usage

### Extract a Theme

```bash
python3 tools/extract_theme.py -i mytheme.db -o ./extracted/
```

This will extract all images and configuration from `mytheme.db` into the `./extracted/` directory.

### Analyze a Theme

Before extracting, you can analyze what's in a theme:

```bash
python3 examples/analyze_theme.py mytheme.db
```

Output:
```
📊 Database Information:
   Format Version: 1
   Total Entries:  42
   File Size:      125.3 KB

🖼️  Images: 18
🎨 Theme Information:
   Name:    My Awesome Theme
   Author:  John Doe
   Version: 1.0
```

## Working with Extracted Data

After extraction, you'll have:

```
extracted/
├── metadata.json              # All metadata
├── theme_info.json           # Parsed theme info
├── extraction_summary.json   # Extraction details
└── images/                   # All extracted images (PNG)
    ├── background.png
    ├── border_top.png
    ├── icon.png
    └── ...
```

### View Theme Information

```bash
cat extracted/theme_info.json
```

```json
{
  "name": "My Awesome Theme",
  "author": "John Doe",
  "version": "1.0",
  "description": "A beautiful E13 theme"
}
```

### Use Extracted Images

The extracted images are standard PNG files:

```bash
# Set as wallpaper (Linux)
feh --bg-scale extracted/images/background.png

# View in image viewer
eog extracted/images/*.png

# Copy to your project
cp extracted/images/*.png /path/to/your/project/
```

## Try the Examples

The repository includes sample themes to test with:

```bash
# Extract sample theme
python3 tools/extract_theme.py \
  -i examples/themes/sample_theme_v1.db \
  -o /tmp/sample_output/

# Check the output
ls -lh /tmp/sample_output/images/
cat /tmp/sample_output/theme_info.json
```

## Batch Processing

Extract multiple themes at once:

```bash
# Extract all themes in a directory
python3 tools/batch_extract.py \
  -i /path/to/themes/ \
  -o ./all_extracted/ \
  --summary batch_results.json

# Or specific files
python3 tools/batch_extract.py \
  -i theme1.db theme2.db theme3.db \
  -o ./output/
```

## Command-Line Options

### extract_theme.py

```bash
python3 tools/extract_theme.py [options]

Required:
  -i, --input PATH      Input DB file
  -o, --output PATH     Output directory

Optional:
  --no-images          Skip image extraction
  --no-config          Skip config extraction
  -v, --verbose        Verbose output
```

### batch_extract.py

```bash
python3 tools/batch_extract.py [options]

Required:
  -i, --input PATH...   Input files or directory
  -o, --output PATH     Base output directory

Optional:
  --summary PATH       Save summary JSON
  -v, --verbose        Verbose output
```

## Common Workflows

### 1. Find Wallpapers

```bash
# Extract theme
python3 tools/extract_theme.py -i theme.db -o /tmp/theme/

# Find backgrounds
ls /tmp/theme/images/ | grep -i "background\|wallpaper\|bg"

# Copy to wallpaper folder
cp /tmp/theme/images/background*.png ~/.local/share/wallpapers/
```

### 2. Extract Icons

```bash
# Extract and find icons
python3 tools/extract_theme.py -i theme.db -o /tmp/theme/
ls /tmp/theme/images/ | grep -i "icon"

# Organize by size (manual or script)
mkdir -p ~/.local/share/icons/e13-theme/48x48/apps/
cp /tmp/theme/images/icon_*.png ~/.local/share/icons/e13-theme/48x48/apps/
```

### 3. Theme Development

```python
#!/usr/bin/env python3
"""Extract theme colors for development"""
import sys
import json
sys.path.append('tools')

from imlib_db_parser import parse_db_file

# Parse theme
theme = parse_db_file('mytheme.db')

# Extract colors from metadata
metadata = {}
for key in theme.get_text_keys():
    if 'color' in key.lower():
        metadata[key] = theme.extract_text(key)

print(json.dumps(metadata, indent=2))
```

## Troubleshooting

### Theme doesn't extract

**Problem**: `Error: File format not recognized`

**Solution**: The file may not be a valid Imlib DB. Try:
```bash
file mytheme.db  # Check file type
hexdump -C mytheme.db | head  # View header
```

### No images found

**Problem**: Extraction succeeds but no images extracted

**Solutions**:
1. Use verbose mode to see what's happening:
   ```bash
   python3 tools/extract_theme.py -i theme.db -o output/ -v
   ```
2. Check metadata for image references:
   ```bash
   cat output/metadata.json
   ```

### Python import errors

**Problem**: `ModuleNotFoundError: No module named 'PIL'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

- **Integration**: See [INTEGRATION.md](INTEGRATION.md) for using extracted themes with KWin, GTK, Qt, etc.
- **API**: See [API.md](API.md) for using the parser in your own code
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Getting Help

- **Issues**: Open an issue on GitHub
- **Examples**: Check the `examples/` directory
- **Documentation**: Read the full README.md

## Learn More

- [Full README](README.md) - Complete documentation
- [API Documentation](API.md) - Programming reference
- [Integration Guide](INTEGRATION.md) - Use with modern desktop environments
