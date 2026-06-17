#!/usr/bin/env python3
"""
Theme Extractor - Extract Enlightenment 0.13 themes from Imlib DB files

This tool extracts images, configuration, and metadata from E13 theme DB files
and converts them to modern formats (PNG, JSON) for use in contemporary desktop
environments like KWin, GTK, Qt, etc.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from imlib_db_parser import ImlibDBParser, ImlibDBError
from semantic_names import SemanticNamer


class ThemeExtractor:
    """Extract and convert E13 theme data to modern formats"""
    
    def __init__(self, output_dir: Path, verbose: bool = False,
                 semantic_names: bool = False):
        """
        Initialize the theme extractor.
        
        Args:
            output_dir: Directory to save extracted files
            verbose: Enable verbose logging
            semantic_names: When True, translate win_* filenames to semantic
                role names using the asset_map.json mapping before saving.
        """
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.semantic_names = semantic_names
        self._namer: Optional[SemanticNamer] = SemanticNamer() if semantic_names else None
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Create output directories
        self.images_dir = self.output_dir / 'images'
        self.icons_dir = self.output_dir / 'icons'
        self.styles_dir = self.output_dir / 'styles'
        
    def extract_theme(self, db_path: Path, 
                     extract_images: bool = True,
                     extract_config: bool = True) -> Dict[str, Any]:
        """
        Extract theme data from a DB file.
        
        Args:
            db_path: Path to the theme DB file
            extract_images: Whether to extract images
            extract_config: Whether to extract configuration
            
        Returns:
            Dictionary with extraction results
        """
        self.logger.info(f"Extracting theme from: {db_path}")
        
        # Parse DB file
        try:
            parser = ImlibDBParser(db_path)
            parser.parse()
        except ImlibDBError as e:
            self.logger.error(f"Failed to parse DB file: {e}")
            return {'success': False, 'error': str(e)}
        
        results = {
            'success': True,
            'db_file': str(db_path),
            'db_version': parser.version,
            'total_entries': len(parser.entries),
            'images_extracted': 0,
            'configs_extracted': 0,
            'metadata': {}
        }
        
        # Extract images
        if extract_images:
            self.logger.info("Extracting images...")
            image_keys = parser.get_image_keys()
            results['images_extracted'] = len(image_keys)
            
            if image_keys:
                self.images_dir.mkdir(parents=True, exist_ok=True)
                for key in image_keys:
                    self._extract_image(parser, key)
            
            self.logger.info(f"Extracted {results['images_extracted']} images")
        
        # Extract configuration and metadata
        if extract_config:
            self.logger.info("Extracting configuration...")
            text_keys = parser.get_text_keys()
            
            metadata = {}
            for key in text_keys:
                text = parser.extract_text(key)
                if text:
                    metadata[key] = text
            
            results['configs_extracted'] = len(metadata)
            results['metadata'] = metadata
            
            # Save metadata to JSON
            if metadata:
                metadata_file = self.output_dir / 'metadata.json'
                self.output_dir.mkdir(parents=True, exist_ok=True)
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                self.logger.info(f"Saved metadata to: {metadata_file}")
            
            # Try to extract theme-specific configuration
            self._extract_theme_config(parser, results)
        
        # Create summary file
        summary_file = self.output_dir / 'extraction_summary.json'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Extraction complete! Summary saved to: {summary_file}")
        return results
    
    def _extract_image(self, parser: ImlibDBParser, key: str) -> None:
        """
        Extract and save an image.
        
        Args:
            parser: Parser instance
            key: Image key
        """
        data = parser.get_entry(key)
        if not data:
            return
        
        # Determine filename from key
        filename = key.replace('/', '_').replace('\\', '_')
        if not any(filename.endswith(ext) for ext in ['.png', '.jpg', '.gif', '.bmp']):
            # Detect format and add extension
            if data.startswith(b'\x89PNG'):
                filename += '.png'
            elif data.startswith(b'\xff\xd8\xff'):
                filename += '.jpg'
            elif data.startswith(b'GIF8'):
                filename += '.gif'
            elif data.startswith(b'BM'):
                filename += '.bmp'
            else:
                filename += '.png'  # Default to PNG

        # Apply semantic naming translation if requested
        if self._namer is not None:
            semantic = self._namer.translate(filename)
            if semantic is not None:
                self.logger.debug(f"Semantic rename: {filename} -> {semantic}")
                filename = semantic
        
        output_path = self.images_dir / filename
        
        # Save image data
        try:
            if PILLOW_AVAILABLE:
                # Use Pillow to convert to PNG for consistency
                from io import BytesIO
                img = Image.open(BytesIO(data))
                # Force convert to PNG
                png_path = output_path.with_suffix('.png')
                img.save(png_path, 'PNG')
                self.logger.debug(f"Saved image: {png_path}")
            else:
                # Save raw image data
                with open(output_path, 'wb') as f:
                    f.write(data)
                self.logger.debug(f"Saved image: {output_path}")
        except Exception as e:
            self.logger.warning(f"Failed to save image {key}: {e}")
    
    def _extract_theme_config(self, parser: ImlibDBParser, results: Dict[str, Any]) -> None:
        """
        Extract E13-specific theme configuration.
        
        Args:
            parser: Parser instance
            results: Results dictionary to update
        """
        # Look for common E13 theme metadata keys
        metadata_keys = [
            'theme/name',
            'theme/author',
            'theme/version',
            'theme/description',
            'theme/license',
            'theme/date',
            '__METADATA__',
            '__INFO__'
        ]
        
        theme_info = {}
        for key in metadata_keys:
            text = parser.extract_text(key)
            if text:
                clean_key = key.split('/')[-1] if '/' in key else key
                theme_info[clean_key] = text
        
        if theme_info:
            results['theme_info'] = theme_info
            
            # Save separate theme info file
            theme_info_file = self.output_dir / 'theme_info.json'
            with open(theme_info_file, 'w') as f:
                json.dump(theme_info, f, indent=2)
            self.logger.info(f"Saved theme info to: {theme_info_file}")
        
        # Extract style configurations
        style_keys = [k for k in parser.get_keys() if 'style' in k.lower() or 'config' in k.lower()]
        if style_keys:
            self.styles_dir.mkdir(parents=True, exist_ok=True)
            styles = {}
            for key in style_keys:
                text = parser.extract_text(key)
                if text:
                    styles[key] = text
                    
                    # Save individual style file
                    style_filename = key.replace('/', '_').replace('\\', '_') + '.txt'
                    style_file = self.styles_dir / style_filename
                    with open(style_file, 'w') as f:
                        f.write(text)
            
            if styles:
                self.logger.info(f"Extracted {len(styles)} style configurations")


def main():
    """Main entry point for the theme extraction tool"""
    parser = argparse.ArgumentParser(
        description='Extract Enlightenment 0.13 theme data from Imlib DB files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all data from a theme
  %(prog)s -i theme.db -o ./extracted/

  # Extract only images
  %(prog)s -i theme.db -o ./output/ --no-config

  # Extract with semantic filenames (win_a_1.ppm -> button_iconify_uns.ppm)
  %(prog)s -i theme.db -o ./output/ --semantic-names

  # Verbose output
  %(prog)s -i theme.db -o ./output/ -v
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        type=Path,
        help='Input Imlib DB/DB2 file'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        type=Path,
        help='Output directory for extracted files'
    )
    
    parser.add_argument(
        '--no-images',
        action='store_true',
        help='Skip image extraction'
    )
    
    parser.add_argument(
        '--no-config',
        action='store_true',
        help='Skip configuration extraction'
    )
    
    parser.add_argument(
        '--semantic-names',
        action='store_true',
        help=(
            'Translate legacy win_* pixmap names to semantic role names '
            '(e.g. win_a_1.ppm -> button_iconify_uns.png) using asset_map.json'
        )
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    if not args.input.is_file():
        print(f"Error: Input path is not a file: {args.input}", file=sys.stderr)
        return 1
    
    # Create extractor and run
    extractor = ThemeExtractor(
        args.output,
        verbose=args.verbose,
        semantic_names=args.semantic_names,
    )
    
    results = extractor.extract_theme(
        args.input,
        extract_images=not args.no_images,
        extract_config=not args.no_config
    )
    
    if not results['success']:
        print(f"Extraction failed: {results.get('error', 'Unknown error')}", file=sys.stderr)
        return 1
    
    print(f"\nExtraction Summary:")
    print(f"  DB Version: {results.get('db_version', 'Unknown')}")
    print(f"  Total Entries: {results['total_entries']}")
    print(f"  Images Extracted: {results['images_extracted']}")
    print(f"  Configs Extracted: {results['configs_extracted']}")
    if args.semantic_names:
        print(f"  Naming mode: semantic (win_* -> role_state.<ext>)")
    print(f"\nOutput saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
