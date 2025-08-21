#!/usr/bin/env python3
"""
Comprehensive script to replace favicon and apple-touch-icon URLs across all HTML files.
Handles various CDN URL patterns and accounts for relative paths in subdirectories.
"""

import os
import re
import glob
from pathlib import Path

def get_relative_path_to_images(file_path):
    """
    Calculate the relative path from the current file to the images directory.
    """
    file_dir = Path(file_path).parent
    images_dir = Path("images")
    
    # Calculate relative path from file directory to images directory
    try:
        relative_path = os.path.relpath(images_dir, file_dir)
        return relative_path
    except ValueError:
        # If we can't calculate relative path, use absolute path
        return "images"

def replace_favicon_urls():
    """
    Replace favicon and apple-touch-icon URLs in all HTML files.
    """
    # Base image filenames
    favicon_filename = "66cbd46970d8568ff4d7ce6f_favicon-32.png"
    apple_touch_icon_filename = "66cbd46c028b52ae6efef671_webclip32.png"
    
    # Find all HTML files recursively
    html_files = glob.glob("**/*.html", recursive=True)
    
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
            
            # Calculate relative path to images for this file
            relative_images_path = get_relative_path_to_images(html_file)
            favicon_path = f"{relative_images_path}/{favicon_filename}"
            apple_touch_icon_path = f"{relative_images_path}/{apple_touch_icon_filename}"
            
            # Pattern 1: Replace any CDN URL containing the favicon filename
            favicon_pattern = r'<link([^>]*?)href="[^"]*' + re.escape(favicon_filename) + r'"[^>]*?rel="shortcut icon"[^>]*?/?>'
            favicon_replacement = f'<link\\1href="{favicon_path}" rel="shortcut icon" type="image/x-icon" />'
            
            # Pattern 2: Replace any CDN URL containing the apple-touch-icon filename
            apple_pattern = r'<link([^>]*?)href="[^"]*' + re.escape(apple_touch_icon_filename) + r'"[^>]*?rel="apple-touch-icon"[^>]*?/?>'
            apple_replacement = f'<link\\1href="{apple_touch_icon_path}" rel="apple-touch-icon" />'
            
            # Apply replacements
            favicon_matches = re.findall(favicon_pattern, content)
            if favicon_matches:
                content = re.sub(favicon_pattern, favicon_replacement, content)
                file_replacements += len(favicon_matches)
                print(f"  - {html_file}: Replaced {len(favicon_matches)} favicon instances")
            
            apple_matches = re.findall(apple_pattern, content)
            if apple_matches:
                content = re.sub(apple_pattern, apple_replacement, content)
                file_replacements += len(apple_matches)
                print(f"  - {html_file}: Replaced {len(apple_matches)} apple-touch-icon instances")
            
            # Write back if content changed
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_modified += 1
                total_replacements += file_replacements
                print(f"✓ Modified: {html_file} ({file_replacements} replacements)")
                print(f"  Paths used: favicon={favicon_path}, apple-touch-icon={apple_touch_icon_path}")
            
            files_processed += 1
            
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")
    print(f"\nBase filenames:")
    print(f"Favicon: {favicon_filename}")
    print(f"Apple touch icon: {apple_touch_icon_filename}")

if __name__ == "__main__":
    replace_favicon_urls()
