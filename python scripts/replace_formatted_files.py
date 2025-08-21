#!/usr/bin/env python3
"""
Replace Original HTML Files with Formatted Versions

This script:
1. Finds all *_formatted.html files
2. Replaces the original HTML files with the formatted versions
3. Removes the *_formatted.html files
4. Preserves the original file names

Usage:
    python3 replace_formatted_files.py [directory]
    python3 replace_formatted_files.py --dry-run [directory]
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


def find_formatted_files(directory: str) -> List[Tuple[str, str]]:
    """
    Find all formatted HTML files and their corresponding original files.
    
    Returns:
        List of tuples: (formatted_file_path, original_file_path)
    """
    formatted_files = []
    directory_path = Path(directory)
    
    # Find all *_formatted.html files recursively
    for formatted_file in directory_path.rglob("*_formatted.html"):
        # Extract original filename by removing "_formatted" suffix
        original_name = formatted_file.stem.replace("_formatted", "")
        original_file = formatted_file.parent / f"{original_name}.html"
        
        formatted_files.append((str(formatted_file), str(original_file)))
    
    return formatted_files


def replace_files(formatted_files: List[Tuple[str, str]], dry_run: bool = False) -> None:
    """
    Replace original files with formatted versions.
    
    Args:
        formatted_files: List of (formatted_file, original_file) tuples
        dry_run: If True, only show what would be done without making changes
    """
    if not formatted_files:
        print("No formatted HTML files found.")
        return
    
    print(f"Found {len(formatted_files)} formatted HTML files to process.")
    print()
    
    for formatted_file, original_file in formatted_files:
        formatted_path = Path(formatted_file)
        original_path = Path(original_file)
        
        if not formatted_path.exists():
            print(f"⚠️  Formatted file not found: {formatted_file}")
            continue
        
        if dry_run:
            if original_path.exists():
                print(f"Would replace: {original_file} ← {formatted_file}")
            else:
                print(f"Would create: {original_file} ← {formatted_file}")
        else:
            try:
                # Remove original file if it exists
                if original_path.exists():
                    original_path.unlink()
                    print(f"🗑️  Removed: {original_file}")
                
                # Rename formatted file to original name
                formatted_path.rename(original_path)
                print(f"✅ Replaced: {original_file}")
                
            except Exception as e:
                print(f"❌ Error processing {formatted_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Replace original HTML files with their formatted versions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 replace_formatted_files.py
  python3 replace_formatted_files.py /path/to/directory
  python3 replace_formatted_files.py --dry-run
  python3 replace_formatted_files.py --dry-run /path/to/directory
        """
    )
    
    parser.add_argument('directory', nargs='?', default='.',
                       help='Directory to process (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.exists(args.directory):
        print(f"❌ Directory does not exist: {args.directory}")
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"❌ Not a directory: {args.directory}")
        sys.exit(1)
    
    # Find formatted files
    formatted_files = find_formatted_files(args.directory)
    
    if not formatted_files:
        print("No *_formatted.html files found in the directory.")
        sys.exit(0)
    
    # Show summary
    print(f"Directory: {args.directory}")
    print(f"Formatted files found: {len(formatted_files)}")
    
    if args.dry_run:
        print("\n=== DRY RUN MODE ===")
        print("No files will be modified. Use without --dry-run to apply changes.")
        print()
    
    # Process files
    replace_files(formatted_files, args.dry_run)
    
    if not args.dry_run:
        print(f"\n✅ Successfully processed {len(formatted_files)} files.")
        print("Original minified HTML files have been replaced with formatted versions.")
    else:
        print(f"\n📋 Dry run completed. {len(formatted_files)} files would be processed.")


if __name__ == "__main__":
    main()
