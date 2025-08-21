#!/usr/bin/env python3
"""
Script to fix broken URLs with page anchors in HTML files.
The issue is URLs like "../index.html\#about" should be "../index.html#about"
"""

import os
import re
import glob
from pathlib import Path

def fix_page_anchor_urls(file_path):
    """
    Fix broken URLs with page anchors in a single HTML file.
    
    Args:
        file_path (str): Path to the HTML file to fix
        
    Returns:
        tuple: (bool, int) - (was_fixed, number_of_fixes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match URLs with backslash before hash
        # This matches href="...\#..." where ... can be any characters
        pattern = r'(href=["\'][^"\']*)\\(#[^"\']*["\'])'
        
        # Find all matches
        matches = re.findall(pattern, content)
        
        if not matches:
            return False, 0
        
        # Replace the pattern: remove the backslash before hash
        fixed_content = re.sub(pattern, r'\1\2', content)
        
        # Write the fixed content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True, len(matches)
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0

def main():
    """
    Main function to process all HTML files in the workspace.
    """
    # Get the current working directory
    workspace_dir = os.getcwd()
    print(f"Working in directory: {workspace_dir}")
    
    # Find all HTML files recursively
    html_files = []
    for pattern in ['**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Statistics
    total_files_processed = 0
    total_files_fixed = 0
    total_fixes = 0
    fixed_files = []
    
    # Process each HTML file
    for file_path in html_files:
        print(f"Processing: {file_path}")
        was_fixed, num_fixes = fix_page_anchor_urls(file_path)
        
        total_files_processed += 1
        if was_fixed:
            total_files_fixed += 1
            total_fixes += num_fixes
            fixed_files.append((file_path, num_fixes))
            print(f"  ✓ Fixed {num_fixes} URLs")
        else:
            print(f"  - No fixes needed")
    
    # Print summary
    print("\n" + "="*60)
    print("FIX SUMMARY")
    print("="*60)
    print(f"Total files processed: {total_files_processed}")
    print(f"Files that needed fixes: {total_files_fixed}")
    print(f"Total URL fixes applied: {total_fixes}")
    
    if fixed_files:
        print("\nFiles that were fixed:")
        for file_path, num_fixes in fixed_files:
            print(f"  {file_path} ({num_fixes} fixes)")
    
    print("\n" + "="*60)
    print("URL fix completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
