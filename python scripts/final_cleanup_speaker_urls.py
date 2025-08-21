#!/usr/bin/env python3
"""
Final cleanup script to remove any remaining escaped characters in speaker page URLs.
"""

import os
import re
import glob
from pathlib import Path

def cleanup_urls(file_path):
    """Clean up any remaining escaped characters in URLs."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove escaped dots in URLs (but preserve legitimate escaped characters)
        # This handles cases like \.html -> .html
        content = re.sub(r'\\\.(?!\w)', '.', content)
        
        # Remove escaped hyphens in URLs
        content = re.sub(r'\\\-', '-', content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all speaker HTML files."""
    # Get the current directory
    current_dir = Path.cwd()
    speakers_dir = current_dir / "speakers"
    zh_speakers_dir = current_dir / "zh" / "speakers"
    
    all_files = []
    
    # Add English speaker files
    if speakers_dir.exists():
        html_files = list(speakers_dir.glob("*.html"))
        all_files.extend(html_files)
        print(f"Found {len(html_files)} English speaker HTML files")
    else:
        print(f"English speakers directory not found: {speakers_dir}")
    
    # Add Chinese speaker files
    if zh_speakers_dir.exists():
        zh_html_files = list(zh_speakers_dir.glob("*.html"))
        all_files.extend(zh_html_files)
        print(f"Found {len(zh_html_files)} Chinese speaker HTML files")
    else:
        print(f"Chinese speakers directory not found: {zh_speakers_dir}")
    
    if not all_files:
        print("No HTML files found in speaker directories")
        return
    
    print(f"Total files to process: {len(all_files)}")
    
    fixed_count = 0
    error_count = 0
    
    for html_file in all_files:
        print(f"Processing: {html_file.name}")
        try:
            if cleanup_urls(html_file):
                print(f"  ✓ Cleaned up URLs in {html_file.name}")
                fixed_count += 1
            else:
                print(f"  - No cleanup needed for {html_file.name}")
        except Exception as e:
            print(f"  ✗ Error processing {html_file.name}: {e}")
            error_count += 1
    
    print(f"\nSummary:")
    print(f"  Total files processed: {len(all_files)}")
    print(f"  Files cleaned up: {fixed_count}")
    print(f"  Files unchanged: {len(all_files) - fixed_count - error_count}")
    print(f"  Errors: {error_count}")

if __name__ == "__main__":
    main()
