#!/usr/bin/env python3
"""
Script to replace social media SVG URLs with local versions.

This script finds all HTML files and replaces CDN URLs for social media icons
with their corresponding local versions in the images directory.
"""

import os
import re
import glob
from pathlib import Path

# Mapping of CDN URLs to local file names
SOCIAL_MEDIA_MAPPINGS = {
    # Hyperlink icon
    r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66bf84acb0f469cc27b2fa33_Hyperlink\\-3\\-\\-Streamline\\-Ultimate\\.svg': 'images/66bf84acb0f469cc27b2fa33_Hyperlink-3--Streamline-Ultimate.svg',
    
    # LinkedIn icon
    r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66bf853720980489a44c58e6_Linkedin\\-Logo\\-\\-Streamline\\-Ultimate\\.svg': 'images/66bf853720980489a44c58e6_Linkedin-Logo--Streamline-Ultimate.svg',
    
    # GitHub icon
    r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66bf8563ca46328f7b53f91b_Github\\-Logo\\-1\\-\\-Streamline\\-Ultimate\\.svg': 'images/66bf8563ca46328f7b53f91b_Github-Logo-1--Streamline-Ultimate.svg',
    
    # X/Twitter icon
    r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66bf857ffde6f20927495260_X\\-Logo\\-\\-Streamline\\-Ultimate\\.svg': 'images/66bf857ffde6f20927495260_X-Logo--Streamline-Ultimate.svg',
    
    # Mastodon icon (note: the CDN URL uses "mastadon" but local file uses "Mastodon")
    r'\.\./cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/66cbd1c3e2cabf9da01cb603_mastadon\\-logo\\.svg': 'images/66ad02e3059014c9b0de5e89_Mastodon-Logo-Fill--Streamline-Phosphor-Fill.svg',
}

def replace_social_media_urls(file_path):
    """
    Replace social media SVG URLs in a single file.
    
    Args:
        file_path (str): Path to the HTML file to process
        
    Returns:
        tuple: (bool, int) - (whether file was modified, number of replacements made)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_replacements = 0
        
        # Apply each replacement pattern
        for pattern, replacement in SOCIAL_MEDIA_MAPPINGS.items():
            # Count matches before replacement
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                total_replacements += len(matches)
                print(f"  - Replaced {len(matches)} instances of {pattern.split('/')[-1]}")
        
        # Write back if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_replacements
        
        return False, 0
        
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False, 0

def main():
    """Main function to process all HTML files."""
    print("Social Media SVG URL Replacement Script")
    print("=" * 50)
    
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', 'zh/*.html', 'speakers/*.html', 'zh/speakers/*.html']:
        html_files.extend(glob.glob(pattern))
    
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    modified_files = 0
    total_replacements = 0
    
    # Process each file
    for file_path in sorted(html_files):
        print(f"Processing: {file_path}")
        was_modified, replacements = replace_social_media_urls(file_path)
        
        if was_modified:
            modified_files += 1
            total_replacements += replacements
            print(f"  ✓ Modified with {replacements} replacements")
        else:
            print(f"  - No changes needed")
        print()
    
    # Summary
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {modified_files}")
    print(f"Total replacements: {total_replacements}")
    
    if modified_files > 0:
        print("\nReplacement mappings used:")
        for pattern, replacement in SOCIAL_MEDIA_MAPPINGS.items():
            filename = pattern.split('/')[-1].replace('\\', '')
            print(f"  {filename} → {replacement}")

if __name__ == "__main__":
    main()
