#!/usr/bin/env python3
"""
Script to fix navigation URLs in speaker pages.
Replaces escaped relative paths (\.\./) with proper relative paths (../)
"""

import os
import re
import glob
from pathlib import Path

def fix_navigation_urls(file_path):
    """Fix navigation URLs in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix escaped relative paths in href attributes
        # Replace \.\./ with ../
        content = re.sub(r'href="\\\.\\\./', 'href="../', content)
        
        # Fix escaped relative paths in src attributes (if any)
        content = re.sub(r'src="\\\.\\\./', 'src="../', content)
        
        # Fix any remaining escaped dots in URLs
        content = re.sub(r'\\\.', '.', content)
        
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
    
    if not speakers_dir.exists():
        print(f"Speakers directory not found: {speakers_dir}")
        return
    
    # Find all HTML files in the speakers directory
    html_files = list(speakers_dir.glob("*.html"))
    
    if not html_files:
        print("No HTML files found in speakers directory")
        return
    
    print(f"Found {len(html_files)} HTML files in speakers directory")
    
    fixed_count = 0
    error_count = 0
    
    for html_file in html_files:
        print(f"Processing: {html_file.name}")
        try:
            if fix_navigation_urls(html_file):
                print(f"  ✓ Fixed navigation URLs in {html_file.name}")
                fixed_count += 1
            else:
                print(f"  - No changes needed for {html_file.name}")
        except Exception as e:
            print(f"  ✗ Error processing {html_file.name}: {e}")
            error_count += 1
    
    print(f"\nSummary:")
    print(f"  Total files processed: {len(html_files)}")
    print(f"  Files fixed: {fixed_count}")
    print(f"  Files unchanged: {len(html_files) - fixed_count - error_count}")
    print(f"  Errors: {error_count}")

if __name__ == "__main__":
    main()
