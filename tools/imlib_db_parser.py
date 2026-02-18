#!/usr/bin/env python3
"""
Imlib DB Parser - Core library for reading Enlightenment 0.13 theme databases

This module provides functionality to parse Imlib DB/DB2 files and extract
images, metadata, and configuration data from Enlightenment 0.13 themes.

The Imlib DB format is a simple key-value database where:
- Keys are strings identifying the data (e.g., "background.png", "metadata/author")
- Values can be image data, text, or binary configuration data
"""

import struct
import io
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path


class ImlibDBError(Exception):
    """Base exception for Imlib DB parsing errors"""
    pass


class ImlibDBParser:
    """
    Parser for Imlib DB/DB2 format files.
    
    The DB format structure:
    - Magic number/header
    - Entry count
    - Index of entries (key, offset, size)
    - Data blocks
    """
    
    # Imlib DB magic numbers
    DB_MAGIC = b'IDB\x00'      # Imlib DB v1
    DB2_MAGIC = b'IDB2'         # Imlib DB v2
    
    def __init__(self, filepath: Path):
        """
        Initialize parser with a DB file path.
        
        Args:
            filepath: Path to the Imlib DB/DB2 file
        """
        self.filepath = Path(filepath)
        self.entries: Dict[str, bytes] = {}
        self.version = None
        
    def parse(self) -> None:
        """
        Parse the DB file and load all entries.
        
        Raises:
            ImlibDBError: If the file format is invalid
        """
        if not self.filepath.exists():
            raise ImlibDBError(f"File not found: {self.filepath}")
            
        with open(self.filepath, 'rb') as f:
            # Read and verify magic number
            magic = f.read(4)
            
            if magic == self.DB_MAGIC:
                self.version = 1
                self._parse_v1(f)
            elif magic == self.DB2_MAGIC:
                self.version = 2
                self._parse_v2(f)
            else:
                # Try alternative parsing for files without clear magic
                f.seek(0)
                self._parse_generic(f)
    
    def _parse_v1(self, f: io.BufferedReader) -> None:
        """Parse Imlib DB version 1 format"""
        # Read entry count
        count_data = f.read(4)
        if len(count_data) < 4:
            raise ImlibDBError("Invalid DB v1 format: cannot read entry count")
        
        entry_count = struct.unpack('>I', count_data)[0]
        
        # Read index
        for _ in range(entry_count):
            # Read key length
            key_len_data = f.read(4)
            if len(key_len_data) < 4:
                break
            key_len = struct.unpack('>I', key_len_data)[0]
            
            # Read key
            key = f.read(key_len).decode('utf-8', errors='replace')
            
            # Read data size
            size_data = f.read(4)
            if len(size_data) < 4:
                break
            size = struct.unpack('>I', size_data)[0]
            
            # Read data
            data = f.read(size)
            self.entries[key] = data
    
    def _parse_v2(self, f: io.BufferedReader) -> None:
        """Parse Imlib DB version 2 format (enhanced with compression support)"""
        # Read flags
        flags_data = f.read(4)
        if len(flags_data) < 4:
            raise ImlibDBError("Invalid DB v2 format: cannot read flags")
        
        flags = struct.unpack('>I', flags_data)[0]
        compressed = flags & 0x01
        
        # Read entry count
        count_data = f.read(4)
        if len(count_data) < 4:
            raise ImlibDBError("Invalid DB v2 format: cannot read entry count")
        
        entry_count = struct.unpack('>I', count_data)[0]
        
        # Read entries
        for _ in range(entry_count):
            # Read key length
            key_len_data = f.read(2)
            if len(key_len_data) < 2:
                break
            key_len = struct.unpack('>H', key_len_data)[0]
            
            # Read key
            key = f.read(key_len).decode('utf-8', errors='replace')
            
            # Read data size
            size_data = f.read(4)
            if len(size_data) < 4:
                break
            size = struct.unpack('>I', size_data)[0]
            
            # Read data
            data = f.read(size)
            
            if compressed:
                try:
                    import zlib
                    data = zlib.decompress(data)
                except:
                    pass  # Keep original data if decompression fails
            
            self.entries[key] = data
    
    def _parse_generic(self, f: io.BufferedReader) -> None:
        """
        Generic parser for DB files without clear magic number.
        Attempts to extract data blocks that look like valid entries.
        """
        content = f.read()
        
        # Try to find image data patterns (PNG, JPEG, etc.)
        patterns = [
            (b'\x89PNG\r\n\x1a\n', '.png'),
            (b'\xff\xd8\xff', '.jpg'),
            (b'GIF89a', '.gif'),
            (b'GIF87a', '.gif'),
            (b'BM', '.bmp'),
        ]
        
        offset = 0
        entry_num = 0
        
        while offset < len(content):
            for pattern, ext in patterns:
                if content[offset:offset+len(pattern)] == pattern:
                    # Find end of image data
                    if ext == '.png':
                        # PNG: Find IEND chunk
                        end = content.find(b'IEND\xaeB`\x82', offset)
                        if end != -1:
                            end += 8
                            key = f"image_{entry_num}{ext}"
                            self.entries[key] = content[offset:end]
                            entry_num += 1
                            offset = end
                            break
                    elif ext == '.jpg':
                        # JPEG: Find EOI marker
                        end = content.find(b'\xff\xd9', offset)
                        if end != -1:
                            end += 2
                            key = f"image_{entry_num}{ext}"
                            self.entries[key] = content[offset:end]
                            entry_num += 1
                            offset = end
                            break
            offset += 1
    
    def get_entry(self, key: str) -> Optional[bytes]:
        """
        Get entry data by key.
        
        Args:
            key: Entry key/identifier
            
        Returns:
            Entry data as bytes, or None if not found
        """
        return self.entries.get(key)
    
    def get_keys(self) -> List[str]:
        """
        Get all entry keys.
        
        Returns:
            List of entry keys
        """
        return list(self.entries.keys())
    
    def get_image_keys(self) -> List[str]:
        """
        Get keys for entries that contain image data.
        
        Returns:
            List of keys for image entries
        """
        image_keys = []
        for key, data in self.entries.items():
            if self._is_image_data(data):
                image_keys.append(key)
        return image_keys
    
    def get_text_keys(self) -> List[str]:
        """
        Get keys for entries that contain text data.
        
        Returns:
            List of keys for text entries
        """
        text_keys = []
        for key, data in self.entries.items():
            if self._is_text_data(data) and not self._is_image_data(data):
                text_keys.append(key)
        return text_keys
    
    def _is_image_data(self, data: bytes) -> bool:
        """Check if data appears to be image data"""
        if len(data) < 4:
            return False
        
        # Check for common image format signatures
        signatures = [
            b'\x89PNG',           # PNG
            b'\xff\xd8\xff',      # JPEG
            b'GIF8',              # GIF
            b'BM',                # BMP
            b'II*\x00',           # TIFF (little-endian)
            b'MM\x00*',           # TIFF (big-endian)
        ]
        
        for sig in signatures:
            if data.startswith(sig):
                return True
        return False
    
    def _is_text_data(self, data: bytes) -> bool:
        """Check if data appears to be text"""
        if len(data) == 0:
            return False
        
        try:
            # Try to decode as UTF-8
            text = data.decode('utf-8')
            # Check if mostly printable ASCII
            printable = sum(c.isprintable() or c in '\n\r\t' for c in text)
            return printable / len(text) > 0.9
        except:
            return False
    
    def extract_text(self, key: str) -> Optional[str]:
        """
        Extract text data from an entry.
        
        Args:
            key: Entry key
            
        Returns:
            Text content, or None if not found or not text
        """
        data = self.get_entry(key)
        if data and self._is_text_data(data):
            return data.decode('utf-8', errors='replace').strip('\x00')
        return None


def parse_db_file(filepath: Path) -> ImlibDBParser:
    """
    Convenience function to parse a DB file.
    
    Args:
        filepath: Path to DB file
        
    Returns:
        Parsed ImlibDBParser instance
    """
    parser = ImlibDBParser(filepath)
    parser.parse()
    return parser
