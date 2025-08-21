#!/usr/bin/env python3
"""
Script to remove all instances of the specific down arrow image element from HTML files.
This targets the image with the specific data-w-id and src attributes.
"""

import os
import re
import glob

def remove_down_arrow_images():
    """Remove all instances of the specific down arrow image element from HTML files."""
    
    # Pattern to match the specific image element
    # This matches the exact image element with the data-w-id and src attributes
    pattern = r'<img width="24" data-w-id="bb2779c9-c325-465d-6ca5-fef762764514" alt="" src="../cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c38565670de1ddefd5f1f8_Down\\-Line\\-\\-Streamline\\-Mingcute\\.svg" loading="lazy"/>'
    
    # Alternative pattern for variations (without data-w-id or with different attributes)
    alt_pattern = r'<img width="24"[^>]*src="../cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66c38565670de1ddefd5f1f8_Down\\-Line\\-\\-Streamline\\-Mingcute\\.svg"[^>]*/>'
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    total_removed = 0
    files_modified = 0
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remove instances matching the main pattern
            content, count1 = re.subn(pattern, '', content)
            
            # Remove instances matching the alternative pattern
            content, count2 = re.subn(alt_pattern, '', content)
            
            total_count = count1 + count2
            
            if total_count > 0:
                # Write the modified content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                total_removed += total_count
                files_modified += 1
                print(f"Removed {total_count} instances from {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nSummary:")
    print(f"Files modified: {files_modified}")
    print(f"Total instances removed: {total_removed}")

if __name__ == "__main__":
    remove_down_arrow_images()
