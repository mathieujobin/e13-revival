#!/usr/bin/env python3
"""
Batch Theme Extractor

Extract multiple E13 theme DB files at once.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import json

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from extract_theme import ThemeExtractor
from imlib_db_parser import ImlibDBError


def batch_extract(input_paths: List[Path], 
                 output_base: Path,
                 verbose: bool = False) -> Dict[str, Any]:
    """
    Extract multiple theme DB files.
    
    Args:
        input_paths: List of DB file paths
        output_base: Base output directory
        verbose: Enable verbose output
        
    Returns:
        Dictionary with batch processing results
    """
    results = {
        'total': len(input_paths),
        'successful': 0,
        'failed': 0,
        'themes': []
    }
    
    for i, db_path in enumerate(input_paths, 1):
        theme_name = db_path.stem
        output_dir = output_base / theme_name
        
        print(f"\n[{i}/{len(input_paths)}] Processing: {theme_name}")
        
        try:
            extractor = ThemeExtractor(output_dir, verbose=verbose)
            theme_results = extractor.extract_theme(db_path)
            
            if theme_results['success']:
                results['successful'] += 1
                print(f"  ✓ Success: {theme_results['images_extracted']} images, "
                      f"{theme_results['configs_extracted']} configs")
                
                results['themes'].append({
                    'name': theme_name,
                    'status': 'success',
                    'images': theme_results['images_extracted'],
                    'configs': theme_results['configs_extracted'],
                    'output': str(output_dir)
                })
            else:
                results['failed'] += 1
                print(f"  ✗ Failed: {theme_results.get('error', 'Unknown error')}")
                
                results['themes'].append({
                    'name': theme_name,
                    'status': 'failed',
                    'error': theme_results.get('error', 'Unknown error')
                })
                
        except Exception as e:
            results['failed'] += 1
            print(f"  ✗ Error: {e}")
            
            results['themes'].append({
                'name': theme_name,
                'status': 'error',
                'error': str(e)
            })
    
    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Batch extract multiple E13 theme DB files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all .db files from a directory
  %(prog)s -i /path/to/themes/ -o ./extracted_themes/
  
  # Extract specific files
  %(prog)s -i theme1.db theme2.db theme3.db -o ./output/
  
  # With verbose output
  %(prog)s -i /path/to/themes/*.db -o ./output/ -v
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        nargs='+',
        help='Input DB file(s) or directory containing DB files'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        type=Path,
        help='Base output directory for extracted themes'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--summary',
        type=Path,
        help='Save batch processing summary to JSON file'
    )
    
    args = parser.parse_args()
    
    # Collect input files
    input_files = []
    for input_spec in args.input:
        input_path = Path(input_spec)
        
        if input_path.is_file() and input_path.suffix == '.db':
            input_files.append(input_path)
        elif input_path.is_dir():
            # Find all .db files in directory
            db_files = list(input_path.glob('*.db'))
            input_files.extend(db_files)
            print(f"Found {len(db_files)} DB files in {input_path}")
        else:
            print(f"Warning: Skipping {input_path} (not a .db file or directory)")
    
    if not input_files:
        print("Error: No valid DB files found")
        return 1
    
    print(f"\nBatch extraction: {len(input_files)} theme(s)")
    print(f"Output directory: {args.output}")
    print("=" * 60)
    
    # Process all files
    results = batch_extract(input_files, args.output, verbose=args.verbose)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Batch Extraction Summary:")
    print(f"  Total:      {results['total']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed:     {results['failed']}")
    
    if results['failed'] > 0:
        print("\nFailed themes:")
        for theme in results['themes']:
            if theme['status'] != 'success':
                print(f"  - {theme['name']}: {theme.get('error', 'Unknown error')}")
    
    # Save summary if requested
    if args.summary:
        with open(args.summary, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nSummary saved to: {args.summary}")
    
    return 0 if results['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
