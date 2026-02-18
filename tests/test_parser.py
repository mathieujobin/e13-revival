"""
Unit tests for Imlib DB parser
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add tools and tests directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
sys.path.insert(0, str(Path(__file__).parent))

from imlib_db_parser import ImlibDBParser, ImlibDBError, parse_db_file
from create_test_db import create_test_db_v1, create_test_db_v2, create_sample_png


class TestImlibDBParser(unittest.TestCase):
    """Test cases for ImlibDBParser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.test_dir_path = Path(self.test_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_parse_db_v1(self):
        """Test parsing DB v1 format"""
        # Create test DB
        entries = {
            'test_key': b'test_value',
            'image.png': create_sample_png(),
        }
        db_path = self.test_dir_path / 'test_v1.db'
        create_test_db_v1(db_path, entries)
        
        # Parse DB
        parser = ImlibDBParser(db_path)
        parser.parse()
        
        # Verify
        self.assertEqual(parser.version, 1)
        self.assertEqual(len(parser.entries), 2)
        self.assertEqual(parser.get_entry('test_key'), b'test_value')
        self.assertTrue(parser.get_entry('image.png').startswith(b'\x89PNG'))
    
    def test_parse_db_v2(self):
        """Test parsing DB v2 format"""
        # Create test DB
        entries = {
            'metadata': b'Some metadata',
            'config': b'Configuration data',
        }
        db_path = self.test_dir_path / 'test_v2.db'
        create_test_db_v2(db_path, entries)
        
        # Parse DB
        parser = ImlibDBParser(db_path)
        parser.parse()
        
        # Verify
        self.assertEqual(parser.version, 2)
        self.assertEqual(len(parser.entries), 2)
        self.assertEqual(parser.get_entry('metadata'), b'Some metadata')
    
    def test_parse_db_v2_compressed(self):
        """Test parsing compressed DB v2 format"""
        # Create test DB with compression
        entries = {
            'large_text': b'A' * 1000,  # Compressible data
        }
        db_path = self.test_dir_path / 'test_v2_compressed.db'
        create_test_db_v2(db_path, entries, compressed=True)
        
        # Parse DB
        parser = ImlibDBParser(db_path)
        parser.parse()
        
        # Verify
        self.assertEqual(parser.version, 2)
        self.assertEqual(parser.get_entry('large_text'), b'A' * 1000)
    
    def test_get_keys(self):
        """Test getting all keys"""
        entries = {
            'key1': b'value1',
            'key2': b'value2',
            'key3': b'value3',
        }
        db_path = self.test_dir_path / 'test_keys.db'
        create_test_db_v1(db_path, entries)
        
        parser = parse_db_file(db_path)
        keys = parser.get_keys()
        
        self.assertEqual(len(keys), 3)
        self.assertIn('key1', keys)
        self.assertIn('key2', keys)
        self.assertIn('key3', keys)
    
    def test_get_image_keys(self):
        """Test identifying image entries"""
        entries = {
            'image1.png': create_sample_png(),
            'text_data': b'Just some text',
            'image2.png': create_sample_png(),
        }
        db_path = self.test_dir_path / 'test_images.db'
        create_test_db_v1(db_path, entries)
        
        parser = parse_db_file(db_path)
        image_keys = parser.get_image_keys()
        
        self.assertEqual(len(image_keys), 2)
        self.assertIn('image1.png', image_keys)
        self.assertIn('image2.png', image_keys)
        self.assertNotIn('text_data', image_keys)
    
    def test_get_text_keys(self):
        """Test identifying text entries"""
        entries = {
            'metadata': b'Theme metadata',
            'image.png': create_sample_png(),
            'config': b'Configuration settings',
        }
        db_path = self.test_dir_path / 'test_text.db'
        create_test_db_v1(db_path, entries)
        
        parser = parse_db_file(db_path)
        text_keys = parser.get_text_keys()
        
        self.assertIn('metadata', text_keys)
        self.assertIn('config', text_keys)
        self.assertNotIn('image.png', text_keys)
    
    def test_extract_text(self):
        """Test text extraction"""
        text_content = 'Theme Name: Test Theme'
        entries = {
            'theme/name': text_content.encode('utf-8'),
        }
        db_path = self.test_dir_path / 'test_extract_text.db'
        create_test_db_v1(db_path, entries)
        
        parser = parse_db_file(db_path)
        extracted = parser.extract_text('theme/name')
        
        self.assertEqual(extracted, text_content)
    
    def test_file_not_found(self):
        """Test error handling for missing file"""
        parser = ImlibDBParser(Path('/nonexistent/file.db'))
        
        with self.assertRaises(ImlibDBError):
            parser.parse()
    
    def test_generic_parser_png(self):
        """Test generic parser with embedded PNG"""
        # Create a file with PNG data but no DB header
        png_data = create_sample_png()
        db_path = self.test_dir_path / 'raw_image.db'
        
        with open(db_path, 'wb') as f:
            f.write(b'JUNK DATA')  # Some junk before
            f.write(png_data)      # PNG data
            f.write(b'MORE JUNK')  # Some junk after
        
        parser = ImlibDBParser(db_path)
        parser.parse()
        
        # Should find the PNG
        image_keys = parser.get_image_keys()
        self.assertGreater(len(image_keys), 0)


if __name__ == '__main__':
    unittest.main()
