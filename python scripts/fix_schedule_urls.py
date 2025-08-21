#!/usr/bin/env python3
"""
Fix escaped backslash URLs in schedule HTML files.
This script replaces URLs like "\.\./speakers/name\.html" with "../speakers/name.html"
"""

import os
import re
import glob

def fix_escaped_urls(file_path):
    """Fix escaped backslash URLs in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix speaker URLs: "\.\./speakers/name\.html" -> "../speakers/name.html"
        content = re.sub(r'\\\.\\\./speakers/([^\\]+)\\\.html', r'../speakers/\1.html', content)
        
        # Fix other relative URLs: "\.\./path\.html" -> "../path.html"
        content = re.sub(r'\\\.\\\./([^\\]+)\\\.html', r'../\1.html', content)
        
        # Fix double escaped URLs: "\.\./\.\./path\.html" -> "../../path.html"
        content = re.sub(r'\\\.\\\./\\\.\\\./([^\\]+)\\\.html', r'../../\1.html', content)
        
        # Fix URLs with escaped hyphens: "name\-surname\.html" -> "name-surname.html"
        content = re.sub(r'([^\\])\\-([^\\])', r'\1-\2', content)
        
        # Fix any remaining escaped dots in URLs
        content = re.sub(r'\\\.', '.', content)
        
        # Fix any remaining escaped slashes in URLs
        content = re.sub(r'\\/', '/', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all schedule HTML files."""
    # Get all HTML files in the schedules folder
    schedule_files = glob.glob('schedules/*.html')
    zh_schedule_files = glob.glob('zh/schedules/*.html')
    
    all_files = schedule_files + zh_schedule_files
    
    print(f"Found {len(all_files)} HTML files to process")
    
    fixed_count = 0
    
    for file_path in all_files:
        if fix_escaped_urls(file_path):
            print(f"Fixed URLs in: {file_path}")
            fixed_count += 1
    
    print(f"\nFixed URLs in {fixed_count} files out of {len(all_files)} total files")

if __name__ == "__main__":
    main()
