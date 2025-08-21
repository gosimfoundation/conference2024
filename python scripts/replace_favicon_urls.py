#!/usr/bin/env python3
"""
Script to replace favicon and apple-touch-icon URLs across all HTML files.
Replaces CDN URLs with local image paths.
"""

import os
import re
import glob
from pathlib import Path

def replace_favicon_urls():
    """
    Replace favicon and apple-touch-icon URLs in all HTML files.
    """
    # Target paths for favicon and apple-touch-icon
    favicon_path = "images/66cbd46970d8568ff4d7ce6f_favicon-32.png"
    apple_touch_icon_path = "images/66cbd46c028b52ae6efef671_webclip32.png"
    
    # Find all HTML files recursively
    html_files = glob.glob("**/*.html", recursive=True)
    
    # Patterns to match and replace
    patterns = [
        # Pattern for shortcut icon (favicon) - matches various CDN URLs
        (
            r'<link[^>]*href="[^"]*66cbd46970d8568ff4d7ce6f_favicon-32\.png"[^>]*rel="shortcut icon"[^>]*/?>',
            f'<link href="{favicon_path}" rel="shortcut icon" type="image/x-icon" />'
        ),
        # Pattern for apple-touch-icon - matches various CDN URLs
        (
            r'<link[^>]*href="[^"]*66cbd46c028b52ae6efef671_webclip32\.png"[^>]*rel="apple-touch-icon"[^>]*/?>',
            f'<link href="{apple_touch_icon_path}" rel="apple-touch-icon" />'
        )
    ]
    
    files_processed = 0
    files_modified = 0
    total_replacements = 0
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_replacements = 0
            
            # Apply each pattern
            for pattern, replacement in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    file_replacements += len(matches)
                    print(f"  - {html_file}: Replaced {len(matches)} instances")
            
            # Write back if content changed
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                total_replacements += file_replacements
                print(f"✓ Modified: {html_file} ({file_replacements} replacements)")
            
            files_processed += 1
            
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")
    print(f"\nFavicon path: {favicon_path}")
    print(f"Apple touch icon path: {apple_touch_icon_path}")

if __name__ == "__main__":
    replace_favicon_urls()
