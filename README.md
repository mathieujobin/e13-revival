# E13 Revival - Enlightenment 0.13 Theme Tools

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This project provides tools for working with Enlightenment 0.13 themes, specifically for extracting and converting legacy Imlib DB/DB2 theme data into modern formats.

## Features

- **Imlib DB Theme Extraction**: Extract images, icons, and configuration data from Enlightenment 0.13 theme files
- **Modern Format Output**: Convert extracted data to PNG (images) and JSON (configuration/metadata)
- **Command-Line Interface**: Easy-to-use CLI tool for batch processing themes
- **Reusable Format**: Output designed for integration with modern desktop environments (KWin, icon themes, etc.)
- **Multiple Format Support**: Handles DB v1, DB v2 (with compression), and generic extraction
- **Batch Processing**: Extract multiple themes at once with summary reporting

## Installation

### Prerequisites

- Python 3.8 or higher
- Imlib2 library (optional, for enhanced image support)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mathieujobin/e13-revival.git
cd e13-revival

# Install dependencies
pip install -r requirements.txt

# Extract a theme
python3 tools/extract_theme.py -i examples/themes/sample_theme_v1.db -o ./output/

# Analyze a theme
python3 examples/analyze_theme.py examples/themes/sample_theme_v1.db
```

See [QUICKSTART.md](QUICKSTART.md) for a detailed quick start guide.

## Usage

### Basic Extraction

```bash
python3 tools/extract_theme.py -i theme.db -o ./output/
```

### Options

- `-i, --input`: Input Imlib DB/DB2 file (required)
- `-o, --output`: Output directory for extracted files (required)
- `--no-images`: Skip image extraction
- `--no-config`: Skip configuration extraction
- `-v, --verbose`: Enable verbose logging

### Examples

```bash
# Extract with verbose output
python3 tools/extract_theme.py -i theme.db -o ./output/ -v

# Extract only images
python3 tools/extract_theme.py -i theme.db -o ./output/ --no-config

# Batch extract multiple themes
python3 tools/batch_extract.py -i themes/*.db -o ./all_themes/
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

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[API Documentation](API.md)** - Complete API reference for developers
- **[Integration Guide](INTEGRATION.md)** - Use with KWin, GTK, Qt, and more
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project

## Development

### Running Tests

```bash
python3 -m unittest discover tests -v
```

### Project Structure

```
e13-revival/
├── tools/              # Core extraction tools
├── tests/              # Unit tests
├── examples/           # Example scripts and sample themes
└── docs/              # Documentation (in .md files)
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Original Enlightenment 0.13 developers
- Imlib/Imlib2 library maintainers
