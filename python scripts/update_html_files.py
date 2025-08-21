#!/usr/bin/env python3
"""
Script to update HTML files to point to local CSS and JS files.
This script will:
1. Update CSS file references to point to css/china2024.css
2. Update jQuery references to point to js/jquery-3.5.1.min.js
3. Update main JS references to point to js/china2024.js
"""

import os
import re
import glob
from pathlib import Path

def get_relative_path(file_path, target_file):
    """
    Calculate the relative path from the HTML file to the target file.
    """
    html_dir = Path(file_path).parent
    target_path = Path(target_file)
    
    # Calculate relative path
    try:
        relative_path = os.path.relpath(target_path, html_dir)
        return relative_path
    except ValueError:
        # If on different drives (Windows), use absolute path
        return target_file

def update_html_file(file_path):
    """
    Update a single HTML file to use local CSS and JS files.
    """
    print(f"Processing: {file_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Calculate relative paths for this file
    css_relative_path = get_relative_path(file_path, "css/china2024.css")
    jquery_relative_path = get_relative_path(file_path, "js/jquery-3.5.1.min.js")
    china2024_js_relative_path = get_relative_path(file_path, "js/china2024.js")
    
    # Update CSS references
    # Pattern to match various CSS link formats
    css_patterns = [
        r'<link[^>]*href=["\'][^"\']*gosim-website[^"\']*\.css["\'][^>]*>',
        r'<link[^>]*href=["\'][^"\']*cdn\.prod\.website-files\.com[^"\']*\.css["\'][^>]*>',
    ]
    
    for pattern in css_patterns:
        content = re.sub(pattern, f'<link href="{css_relative_path}" rel="stylesheet" type="text/css" />', content)
    
    # Update jQuery references
    # Pattern to match jQuery script tags
    jquery_patterns = [
        r'<script[^>]*src=["\'][^"\']*jquery-3\.5\.1\.min[^"\']*["\'][^>]*></script>',
        r'<script[^>]*src=["\'][^"\']*d3e54v103j8qbb\.cloudfront\.net[^"\']*jquery[^"\']*["\'][^>]*></script>',
    ]
    
    for pattern in jquery_patterns:
        content = re.sub(pattern, f'<script src="{jquery_relative_path}" type="text/javascript"></script>', content)
    
    # Update main JS references
    # Pattern to match main JS script tags
    js_patterns = [
        r'<script[^>]*src=["\'][^"\']*gosim-website[^"\']*\.js["\'][^>]*></script>',
        r'<script[^>]*src=["\'][^"\']*cdn\.prod\.website-files\.com[^"\']*\.js["\'][^>]*></script>',
    ]
    
    for pattern in js_patterns:
        content = re.sub(pattern, f'<script src="{china2024_js_relative_path}" type="text/javascript"></script>', content)
    
    # Write back to file if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated: {file_path}")
        return True
    else:
        print(f"  - No changes needed: {file_path}")
        return False

def main():
    """
    Main function to process all HTML files.
    """
    # Find all HTML files recursively
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 50)
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            if update_html_file(html_file):
                updated_count += 1
        except Exception as e:
            print(f"  ✗ Error processing {html_file}: {e}")
    
    print("=" * 50)
    print(f"Processing complete!")
    print(f"Files updated: {updated_count}")
    print(f"Files unchanged: {len(html_files) - updated_count}")

if __name__ == "__main__":
    main()
