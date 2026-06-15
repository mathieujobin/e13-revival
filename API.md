# API Documentation

## Module: `imlib_db_parser`

The core module for parsing Enlightenment 0.13 Imlib DB/DB2 files.

### Classes

#### `ImlibDBError`

Exception raised when there are errors parsing DB files.

**Inheritance**: `Exception`

**Example**:
```python
try:
    parser.parse()
except ImlibDBError as e:
    print(f"Error: {e}")
```

---

#### `ImlibDBParser`

Main parser class for Imlib DB/DB2 format files.

##### Constructor

```python
ImlibDBParser(filepath: Path)
```

**Parameters**:
- `filepath` (Path): Path to the Imlib DB/DB2 file

**Example**:
```python
from pathlib import Path
from imlib_db_parser import ImlibDBParser

parser = ImlibDBParser(Path('theme.db'))
```

##### Attributes

- `filepath` (Path): Path to the DB file
- `entries` (Dict[str, bytes]): Dictionary of parsed entries (key -> data)
- `version` (int | None): DB format version (1 or 2), None if generic parsing

##### Methods

###### `parse() -> None`

Parse the DB file and load all entries into memory.

**Raises**:
- `ImlibDBError`: If the file doesn't exist or format is invalid

**Example**:
```python
parser = ImlibDBParser(Path('theme.db'))
parser.parse()
print(f"Loaded {len(parser.entries)} entries")
```

---

###### `get_entry(key: str) -> Optional[bytes]`

Get the raw data for a specific entry.

**Parameters**:
- `key` (str): Entry identifier/key

**Returns**:
- `bytes | None`: Entry data, or None if not found

**Example**:
```python
data = parser.get_entry('background.png')
if data:
    with open('background.png', 'wb') as f:
        f.write(data)
```

---

###### `get_keys() -> List[str]`

Get all entry keys in the database.

**Returns**:
- `List[str]`: List of all entry keys

**Example**:
```python
keys = parser.get_keys()
print(f"Available keys: {', '.join(keys)}")
```

---

###### `get_image_keys() -> List[str]`

Get keys for entries that contain image data.

The method detects images by checking for common format signatures (PNG, JPEG, GIF, BMP, TIFF).

**Returns**:
- `List[str]`: List of keys for image entries

**Example**:
```python
image_keys = parser.get_image_keys()
for key in image_keys:
    data = parser.get_entry(key)
    # Process image data
```

---

###### `get_text_keys() -> List[str]`

Get keys for entries that contain text data.

The method identifies text by attempting UTF-8 decoding and checking for printable characters.

**Returns**:
- `List[str]`: List of keys for text entries

**Example**:
```python
text_keys = parser.get_text_keys()
for key in text_keys:
    text = parser.extract_text(key)
    print(f"{key}: {text}")
```

---

###### `extract_text(key: str) -> Optional[str]`

Extract and decode text data from an entry.

**Parameters**:
- `key` (str): Entry key

**Returns**:
- `str | None`: Decoded text content, or None if not found or not text

**Example**:
```python
theme_name = parser.extract_text('theme/name')
if theme_name:
    print(f"Theme: {theme_name}")
```

---

### Functions

#### `parse_db_file(filepath: Path) -> ImlibDBParser`

Convenience function to parse a DB file in one call.

**Parameters**:
- `filepath` (Path): Path to DB file

**Returns**:
- `ImlibDBParser`: Parsed parser instance with entries loaded

**Example**:
```python
from imlib_db_parser import parse_db_file
from pathlib import Path

parser = parse_db_file(Path('theme.db'))
images = parser.get_image_keys()
```

---

## Module: `extract_theme`

Command-line tool and API for extracting theme data.

### Classes

#### `ThemeExtractor`

High-level theme extraction and conversion tool.

##### Constructor

```python
ThemeExtractor(output_dir: Path, verbose: bool = False)
```

**Parameters**:
- `output_dir` (Path): Directory to save extracted files
- `verbose` (bool): Enable verbose logging (default: False)

**Example**:
```python
from pathlib import Path
from extract_theme import ThemeExtractor

extractor = ThemeExtractor(Path('./output'), verbose=True)
```

##### Methods

###### `extract_theme(db_path: Path, extract_images: bool = True, extract_config: bool = True) -> Dict[str, Any]`

Extract theme data from a DB file.

**Parameters**:
- `db_path` (Path): Path to the theme DB file
- `extract_images` (bool): Whether to extract images (default: True)
- `extract_config` (bool): Whether to extract configuration (default: True)

**Returns**:
- `Dict[str, Any]`: Dictionary with extraction results containing:
  - `success` (bool): Whether extraction succeeded
  - `db_file` (str): Path to source DB file
  - `db_version` (int): DB format version
  - `total_entries` (int): Total number of entries
  - `images_extracted` (int): Number of images extracted
  - `configs_extracted` (int): Number of config entries extracted
  - `metadata` (dict): Extracted metadata
  - `theme_info` (dict): Parsed theme information (if available)
  - `error` (str): Error message (only if success=False)

**Example**:
```python
from pathlib import Path
from extract_theme import ThemeExtractor

extractor = ThemeExtractor(Path('./output'))
results = extractor.extract_theme(Path('theme.db'))

if results['success']:
    print(f"Extracted {results['images_extracted']} images")
    print(f"Theme: {results['theme_info'].get('name', 'Unknown')}")
else:
    print(f"Error: {results['error']}")
```

---

## Data Formats

### DB File Formats

#### DB v1 Format

Binary structure:
```
[4 bytes] Magic: 'IDB\0'
[4 bytes] Entry count (big-endian)
For each entry:
  [4 bytes] Key length (big-endian)
  [N bytes] Key (UTF-8 string)
  [4 bytes] Data size (big-endian)
  [M bytes] Data
```

#### DB v2 Format

Binary structure:
```
[4 bytes] Magic: 'IDB2'
[4 bytes] Flags (big-endian)
          bit 0: compression flag
[4 bytes] Entry count (big-endian)
For each entry:
  [2 bytes] Key length (big-endian)
  [N bytes] Key (UTF-8 string)
  [4 bytes] Data size (big-endian)
  [M bytes] Data (possibly compressed with zlib)
```

### Output Formats

#### metadata.json

Contains all text entries from the DB file.

```json
{
  "theme/name": "Theme Name",
  "theme/author": "Author Name",
  "theme/version": "1.0",
  "theme/description": "Theme description",
  "config/key": "value"
}
```

#### theme_info.json

Extracted and parsed theme-specific metadata.

```json
{
  "name": "Theme Name",
  "author": "Author Name",
  "version": "1.0",
  "description": "Theme description",
  "license": "GPL-2.0",
  "date": "2000-01-01"
}
```

#### extraction_summary.json

Summary of the extraction process.

```json
{
  "success": true,
  "db_file": "path/to/theme.db",
  "db_version": 1,
  "total_entries": 42,
  "images_extracted": 15,
  "configs_extracted": 27,
  "metadata": { ... },
  "theme_info": { ... }
}
```

---

## Complete Examples

### Example 1: Extract All Data

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append('tools')

from imlib_db_parser import parse_db_file
from extract_theme import ThemeExtractor

# Parse DB file
db_file = Path('mytheme.db')
parser = parse_db_file(db_file)

print(f"DB version: {parser.version}")
print(f"Total entries: {len(parser.entries)}")
print(f"Images: {len(parser.get_image_keys())}")
print(f"Text entries: {len(parser.get_text_keys())}")

# Extract to directory
extractor = ThemeExtractor(Path('./extracted'), verbose=True)
results = extractor.extract_theme(db_file)

if results['success']:
    print(f"\nExtraction successful!")
    print(f"Images: {results['images_extracted']}")
    print(f"Configs: {results['configs_extracted']}")
```

### Example 2: Extract Specific Images

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append('tools')

from imlib_db_parser import parse_db_file

# Parse and find images
parser = parse_db_file(Path('theme.db'))

# Look for specific image types
backgrounds = [k for k in parser.get_image_keys() if 'background' in k.lower()]
borders = [k for k in parser.get_image_keys() if 'border' in k.lower()]

print(f"Found {len(backgrounds)} backgrounds")
print(f"Found {len(borders)} borders")

# Extract backgrounds
output_dir = Path('./backgrounds')
output_dir.mkdir(exist_ok=True)

for key in backgrounds:
    data = parser.get_entry(key)
    filename = key.replace('/', '_')
    with open(output_dir / filename, 'wb') as f:
        f.write(data)
    print(f"Extracted: {filename}")
```

### Example 3: Read Theme Metadata

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append('tools')

from imlib_db_parser import parse_db_file

parser = parse_db_file(Path('theme.db'))

# Extract theme information
metadata = {}
for key in parser.get_text_keys():
    text = parser.extract_text(key)
    if text:
        metadata[key] = text

# Display theme info
print("Theme Information:")
print(f"  Name: {metadata.get('theme/name', 'Unknown')}")
print(f"  Author: {metadata.get('theme/author', 'Unknown')}")
print(f"  Version: {metadata.get('theme/version', 'Unknown')}")
print(f"  Description: {metadata.get('theme/description', 'N/A')}")

# Show all metadata
print("\nAll Metadata:")
for key, value in metadata.items():
    print(f"  {key}: {value}")
```

### Example 4: Batch Processing

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append('tools')

from extract_theme import ThemeExtractor

# Process all DB files in a directory
themes_dir = Path('/path/to/themes')
output_base = Path('./extracted_themes')

for db_file in themes_dir.glob('*.db'):
    theme_name = db_file.stem
    output_dir = output_base / theme_name
    
    print(f"\nProcessing: {theme_name}")
    extractor = ThemeExtractor(output_dir)
    results = extractor.extract_theme(db_file)
    
    if results['success']:
        print(f"  ✓ Success: {results['images_extracted']} images")
    else:
        print(f"  ✗ Failed: {results['error']}")
```

---

## Error Handling

### Common Errors

#### File Not Found
```python
try:
    parser = ImlibDBParser(Path('missing.db'))
    parser.parse()
except ImlibDBError as e:
    print(f"Error: {e}")  # "File not found: missing.db"
```

#### Invalid Format
```python
try:
    parser = ImlibDBParser(Path('invalid.db'))
    parser.parse()
except ImlibDBError as e:
    print(f"Parsing error: {e}")
```

### Graceful Degradation

The parser includes fallback mechanisms:

1. **Generic Parser**: If DB magic number is not recognized, attempts to extract embedded images
2. **Compression Handling**: Automatically detects and decompresses v2 compressed data
3. **Encoding Handling**: Uses UTF-8 with error replacement for text data

---

## Performance Considerations

- **Memory**: Parser loads entire DB into memory - suitable for typical theme files (<100MB)
- **Speed**: Parsing is fast - typically <100ms for small themes, <1s for large ones
- **I/O**: Images are extracted synchronously - consider parallel processing for batch operations

---

## Extending the Tool

### Adding New Format Support

To support additional image formats in the generic parser:

```python
# In imlib_db_parser.py, _parse_generic method
patterns = [
    (b'\x89PNG\r\n\x1a\n', '.png'),
    (b'\xff\xd8\xff', '.jpg'),
    # Add your format:
    (b'YOUR_MAGIC', '.ext'),
]
```

### Custom Extraction Logic

Extend `ThemeExtractor` for custom processing:

```python
from extract_theme import ThemeExtractor

class CustomExtractor(ThemeExtractor):
    def _extract_image(self, parser, key):
        # Custom image processing
        data = parser.get_entry(key)
        # ... your logic ...
        super()._extract_image(parser, key)
```

---

## Version History

- **v1.0** (2026-02): Initial release with DB v1/v2 support, image extraction, metadata extraction
