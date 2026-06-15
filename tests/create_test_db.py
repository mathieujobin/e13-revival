"""
Test utilities for creating sample Imlib DB files for testing
"""

import struct
from pathlib import Path
from typing import Dict


def create_test_db_v1(output_path: Path, entries: Dict[str, bytes]) -> None:
    """
    Create a test Imlib DB v1 file.
    
    Args:
        output_path: Path to save the DB file
        entries: Dictionary of key-value pairs to store
    """
    with open(output_path, 'wb') as f:
        # Write magic number
        f.write(b'IDB\x00')
        
        # Write entry count
        f.write(struct.pack('>I', len(entries)))
        
        # Write entries
        for key, data in entries.items():
            key_bytes = key.encode('utf-8')
            
            # Write key length
            f.write(struct.pack('>I', len(key_bytes)))
            
            # Write key
            f.write(key_bytes)
            
            # Write data size
            f.write(struct.pack('>I', len(data)))
            
            # Write data
            f.write(data)


def create_test_db_v2(output_path: Path, entries: Dict[str, bytes], compressed: bool = False) -> None:
    """
    Create a test Imlib DB v2 file.
    
    Args:
        output_path: Path to save the DB file
        entries: Dictionary of key-value pairs to store
        compressed: Whether to compress the data
    """
    with open(output_path, 'wb') as f:
        # Write magic number
        f.write(b'IDB2')
        
        # Write flags
        flags = 0x01 if compressed else 0x00
        f.write(struct.pack('>I', flags))
        
        # Write entry count
        f.write(struct.pack('>I', len(entries)))
        
        # Write entries
        for key, data in entries.items():
            key_bytes = key.encode('utf-8')
            
            if compressed:
                import zlib
                data = zlib.compress(data)
            
            # Write key length (16-bit for v2)
            f.write(struct.pack('>H', len(key_bytes)))
            
            # Write key
            f.write(key_bytes)
            
            # Write data size
            f.write(struct.pack('>I', len(data)))
            
            # Write data
            f.write(data)


def create_sample_png() -> bytes:
    """Create a minimal valid PNG image for testing"""
    # Minimal 1x1 red PNG
    png_data = (
        b'\x89PNG\r\n\x1a\n'  # PNG signature
        b'\x00\x00\x00\rIHDR'  # IHDR chunk
        b'\x00\x00\x00\x01'    # Width: 1
        b'\x00\x00\x00\x01'    # Height: 1
        b'\x08\x02\x00\x00\x00'  # Bit depth, color type, etc.
        b'\x90wS\xde'          # CRC
        b'\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01'  # IDAT chunk
        b'\x00\x18\xdd\x8d\xb4'  # CRC
        b'\x00\x00\x00\x00IEND\xaeB`\x82'  # IEND chunk
    )
    return png_data


def create_sample_jpeg() -> bytes:
    """Create a minimal valid JPEG image for testing"""
    # Minimal JPEG (1x1 black pixel)
    jpeg_data = (
        b'\xff\xd8\xff\xe0'      # SOI + APP0
        b'\x00\x10JFIF\x00\x01'  # JFIF header
        b'\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xff\xdb\x00C'         # DQT
        b'\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c'
        b'\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444'
        b'\x1f\x27\x1c\x1c\x1c\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00'
        b'\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\xff\xda\x00\x08\x01\x01\x00\x00?\x00\x7f\xff\xd9'  # SOS + EOI
    )
    return jpeg_data


if __name__ == '__main__':
    # Create sample test files
    import sys
    from pathlib import Path
    
    # Create examples directory
    examples_dir = Path(__file__).parent.parent / 'examples' / 'themes'
    examples_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample DB v1 with images and metadata
    entries = {
        'background.png': create_sample_png(),
        'icon.png': create_sample_png(),
        'border_top.png': create_sample_png(),
        'theme/name': b'Sample Theme',
        'theme/author': b'E13 Revival Team',
        'theme/version': b'1.0',
        'theme/description': b'A sample theme for testing the extraction tool',
    }
    
    create_test_db_v1(examples_dir / 'sample_theme_v1.db', entries)
    print(f"Created sample DB v1: {examples_dir / 'sample_theme_v1.db'}")
    
    # Create sample DB v2
    create_test_db_v2(examples_dir / 'sample_theme_v2.db', entries)
    print(f"Created sample DB v2: {examples_dir / 'sample_theme_v2.db'}")
    
    # Create sample DB v2 with compression
    create_test_db_v2(examples_dir / 'sample_theme_v2_compressed.db', entries, compressed=True)
    print(f"Created sample DB v2 (compressed): {examples_dir / 'sample_theme_v2_compressed.db'}")
