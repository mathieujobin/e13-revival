# E13 Revival - Enlightenment 0.13 Theme Tools

This project provides tools for working with Enlightenment 0.13 themes, specifically for extracting and converting legacy Imlib DB/DB2 theme data into modern formats.

## Features

- **Imlib DB Theme Extraction**: Extract images, icons, and configuration data from Enlightenment 0.13 theme files
- **Modern Format Output**: Convert extracted data to PNG (images) and JSON (configuration/metadata)
- **Command-Line Interface**: Easy-to-use CLI tool for batch processing themes
- **Reusable Format**: Output designed for integration with modern desktop environments (KWin, icon themes, etc.)

## Installation

### Prerequisites

- Python 3.8 or higher
- Imlib2 library (optional, for enhanced image support)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Extract Theme Data

```bash
python tools/extract_theme.py --input /path/to/theme.db --output /path/to/output/
```

### Options

- `--input, -i`: Input Imlib DB/DB2 file or directory
- `--output, -o`: Output directory for extracted files
- `--format`: Output format (json, yaml) for metadata (default: json)
- `--extract-images`: Extract images as PNG files (default: true)
- `--extract-config`: Extract configuration data (default: true)
- `--verbose, -v`: Enable verbose logging

### Example

```bash
# Extract a complete theme
python tools/extract_theme.py -i ~/.enlightenment/themes/MyTheme.db -o ./extracted/MyTheme/

# Extract only images
python tools/extract_theme.py -i theme.db -o ./output/ --extract-config=false

# Verbose output
python tools/extract_theme.py -i theme.db -o ./output/ -v
```

## Output Structure

```
output/
├── metadata.json          # Theme metadata and configuration
├── images/               # Extracted images
│   ├── background.png
│   ├── border_*.png
│   └── ...
├── icons/                # Extracted icons
│   └── ...
└── styles/              # Extracted style configurations
    └── ...
```

## Imlib DB Format

Enlightenment 0.13 used Imlib's database format to store theme data. The DB files contain:

- **Images**: Stored in various formats (PNG, JPEG, etc.)
- **Metadata**: Theme name, author, version
- **Configuration**: Widget styles, colors, borders
- **Icons**: Application and file type icons

## Integration

The extracted theme data can be used with:

- **KWin**: Window decoration themes
- **Icon Themes**: Desktop icon sets
- **GTK/Qt Themes**: Application styling
- **Wallpapers**: Desktop backgrounds

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
black tools/ tests/
flake8 tools/ tests/
```

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Original Enlightenment 0.13 developers
- Imlib/Imlib2 library maintainers
