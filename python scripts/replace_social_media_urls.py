#!/usr/bin/env python3
"""
Script to replace social media icon URLs in HTML files with local image paths.
"""

import os
import re
import glob
from pathlib import Path

def replace_urls_in_file(file_path):
    """
    Replace the specified URLs in a single HTML file.
    
    Args:
        file_path (str): Path to the HTML file to process
        
    Returns:
        tuple: (bool, int) - (was_modified, number_of_replacements)
    """
    replacements = {
        # X (Twitter) logo replacement
        r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66ad02e384b9dea8d976b7cd_X-Logo-Fill--Streamline-Phosphor-Fill\.svg': 
        'images/66bf857ffde6f20927495260_X-Logo--Streamline-Ultimate.svg',
        
        # Mastodon logo replacement
        r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66ad02e3059014c9b0de5e89_Mastodon-Logo-Fill--Streamline-Phosphor-Fill\.svg': 
        'images/66cbd1c3e2cabf9da01cb603_mastadon-logo.svg'
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_replacements = 0
        
        for pattern, replacement in replacements.items():
            # Count matches before replacement
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                total_replacements += len(matches)
                print(f"  - Replaced {len(matches)} instance(s) of {pattern.split('/')[-1]}")
        
        # Write back to file if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_replacements
        else:
            return False, 0
            
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False, 0

def main():
    """
    Main function to process all HTML files in the workspace.
    """
    print("Starting social media URL replacement...")
    print("=" * 50)
    
    # Find all HTML files in the current directory and subdirectories
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    # Remove duplicates and sort
    html_files = sorted(list(set(html_files)))
    
    if not html_files:
        print("No HTML files found in the current directory.")
        return
    
    print(f"Found {len(html_files)} HTML file(s) to process:")
    print()
    
    total_files_modified = 0
    total_replacements = 0
    
    for file_path in html_files:
        print(f"Processing: {file_path}")
        was_modified, replacements = replace_urls_in_file(file_path)
        
        if was_modified:
            total_files_modified += 1
            total_replacements += replacements
            print(f"  ✓ Modified ({replacements} replacement(s))")
        else:
            print(f"  - No changes needed")
        print()
    
    print("=" * 50)
    print(f"Summary:")
    print(f"  - Files processed: {len(html_files)}")
    print(f"  - Files modified: {total_files_modified}")
    print(f"  - Total replacements: {total_replacements}")
    
    if total_replacements > 0:
        print(f"\n✓ Successfully replaced {total_replacements} URL(s) across {total_files_modified} file(s)")
    else:
        print(f"\n- No URLs were found to replace")

if __name__ == "__main__":
    main()
