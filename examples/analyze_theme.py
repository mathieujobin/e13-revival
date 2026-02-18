#!/usr/bin/env python3
"""
Example: Quick theme analyzer

Analyzes an E13 theme DB file and displays information about its contents.
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from imlib_db_parser import parse_db_file, ImlibDBError


def analyze_theme(db_path: Path) -> None:
    """Analyze and display theme information"""
    
    print(f"Analyzing theme: {db_path.name}")
    print("=" * 60)
    
    try:
        # Parse the DB file
        parser = parse_db_file(db_path)
        
        # Basic info
        print(f"\n📊 Database Information:")
        print(f"   Format Version: {parser.version if parser.version else 'Generic'}")
        print(f"   Total Entries:  {len(parser.entries)}")
        print(f"   File Size:      {db_path.stat().st_size / 1024:.1f} KB")
        
        # Images
        image_keys = parser.get_image_keys()
        print(f"\n🖼️  Images: {len(image_keys)}")
        if image_keys:
            print(f"   Sample images:")
            for key in image_keys[:5]:  # Show first 5
                data = parser.get_entry(key)
                print(f"     - {key} ({len(data)} bytes)")
            if len(image_keys) > 5:
                print(f"     ... and {len(image_keys) - 5} more")
        
        # Text/metadata
        text_keys = parser.get_text_keys()
        print(f"\n📝 Text Entries: {len(text_keys)}")
        if text_keys:
            for key in text_keys:
                text = parser.extract_text(key)
                if text:
                    # Truncate long text
                    display_text = text[:50] + "..." if len(text) > 50 else text
                    print(f"   {key}: {display_text}")
        
        # Theme info
        theme_name = parser.extract_text('theme/name')
        theme_author = parser.extract_text('theme/author')
        theme_version = parser.extract_text('theme/version')
        
        if theme_name or theme_author or theme_version:
            print(f"\n🎨 Theme Information:")
            if theme_name:
                print(f"   Name:    {theme_name}")
            if theme_author:
                print(f"   Author:  {theme_author}")
            if theme_version:
                print(f"   Version: {theme_version}")
        
        # Image type breakdown
        if image_keys:
            print(f"\n📷 Image Types:")
            png_count = sum(1 for k in image_keys if parser.get_entry(k).startswith(b'\x89PNG'))
            jpg_count = sum(1 for k in image_keys if parser.get_entry(k).startswith(b'\xff\xd8\xff'))
            gif_count = sum(1 for k in image_keys if parser.get_entry(k).startswith(b'GIF8'))
            other_count = len(image_keys) - png_count - jpg_count - gif_count
            
            if png_count:
                print(f"   PNG:   {png_count}")
            if jpg_count:
                print(f"   JPEG:  {jpg_count}")
            if gif_count:
                print(f"   GIF:   {gif_count}")
            if other_count:
                print(f"   Other: {other_count}")
        
        print(f"\n✅ Analysis complete!")
        print(f"\nTo extract this theme, run:")
        print(f"   python3 tools/extract_theme.py -i {db_path} -o ./output/")
        
    except ImlibDBError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: analyze_theme.py <theme.db>")
        print("\nExample:")
        print("  python3 examples/analyze_theme.py examples/themes/sample_theme_v1.db")
        return 1
    
    db_path = Path(sys.argv[1])
    
    if not db_path.exists():
        print(f"Error: File not found: {db_path}")
        return 1
    
    if not db_path.is_file():
        print(f"Error: Not a file: {db_path}")
        return 1
    
    return analyze_theme(db_path)


if __name__ == '__main__':
    sys.exit(main())
