#!/usr/bin/env python3
"""
Script to replace CDN logo URLs with localized versions.
Replaces: ../cdn.prod.website-files.com/667a2b77418bcfe1656798ef/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg
With: images/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg
"""

import os
import re
import glob
from pathlib import Path

def replace_logo_urls():
    """
    Replace all instances of the CDN logo URL with the localized version.
    """
    # Define the patterns to search for and replace
    old_patterns = [
        r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c7dd4f6865e5012249f0d5_gosim-logo-32\.svg',
        r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c7dd4f6865e5012249f0d5_gosim\\-logo\\-32\\.svg',
        r'cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c7dd4f6865e5012249f0d5_gosim-logo-32\.svg',
        r'cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c7dd4f6865e5012249f0d5_gosim\\-logo\\-32\\.svg'
    ]
    
    new_url = 'images/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg'
    
    # Find all HTML files in the current directory and subdirectories
    html_files = glob.glob('**/*.html', recursive=True)
    
    total_replacements = 0
    files_modified = []
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_replacements = 0
            
            # Apply each pattern replacement
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, new_url, content)
                    file_replacements += len(matches)
                    print(f"  Found {len(matches)} matches in {file_path} using pattern: {pattern}")
            
            # Write back if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_modified.append(file_path)
                total_replacements += file_replacements
                print(f"✓ Modified {file_path} ({file_replacements} replacements)")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total files modified: {len(files_modified)}")
    print(f"Total replacements made: {total_replacements}")
    
    if files_modified:
        print(f"\nModified files:")
        for file_path in files_modified:
            print(f"  - {file_path}")
    
    # Verify the logo file exists
    logo_path = Path('images/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg')
    if logo_path.exists():
        print(f"\n✓ Local logo file exists: {logo_path}")
    else:
        print(f"\n⚠ Warning: Local logo file not found: {logo_path}")

if __name__ == "__main__":
    print("Logo URL Replacement Script")
    print("=" * 40)
    replace_logo_urls()
    print("\nScript completed!")
