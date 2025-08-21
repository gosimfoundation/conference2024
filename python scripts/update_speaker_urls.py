#!/usr/bin/env python3
"""
Script to update all speaker HTML files with correct relative URLs.
This script applies the same URL changes that were made to alan-majer.html
to all other speaker files in the speakers/ directory.
"""

import os
import re
import glob

def update_speaker_urls():
    """Update all speaker HTML files with correct relative URLs."""
    
    # Get all HTML files in the speakers directory
    speaker_files = glob.glob("speakers/*.html")
    
    # URL patterns to replace
    url_replacements = [
        # CSS file
        (r'href="css/china2024\.css"', 'href="../css/china2024.css"'),
        
        # Favicon and webclip
        (r'href="images/66cbd46970d8568ff4d7ce6f_favicon-32\.png"', 'href="../images/66cbd46970d8568ff4d7ce6f_favicon-32.png"'),
        (r'href="images/66cbd46c028b52ae6efef671_webclip32\.png"', 'href="../images/66cbd46c028b52ae6efef671_webclip32.png"'),
        
        # Logo URLs (handle escaped patterns)
        (r'src="\\\.\\\./images/66c7dd4f6865e5012249f0d5_gosim-logo-32\.svg"', 'src="../images/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg"'),
        (r'src="images/66c7dd4f6865e5012249f0d5_gosim-logo-32\.svg"', 'src="../images/66c7dd4f6865e5012249f0d5_gosim-logo-32.svg"'),
        
        # Speaker background images (fix incorrect ../../images/speakers/)
        (r'url\(\.\./\.\./images/speakers/', 'url(../images/speakers/'),
        (r'url\(images/speakers/', 'url(../images/speakers/'),
        
        # Social media icons (handle escaped patterns)
        (r'src="\\\.\\\./images/([^"]+)"', r'src="../images/\1"'),
        (r'src="images/([^"]+)"', r'src="../images/\1"'),
        
        # JavaScript files
        (r'src="js/jquery-3\.5\.1\.min\.js"', 'src="../js/jquery-3.5.1.min.js"'),
        (r'src="js/china2024\.js"', 'src="../js/china2024.js"'),
        
        # Navigation links (add ../ prefix)
        (r'href="index\.html"', 'href="../index.html"'),
        (r'href="schedule\.html"', 'href="../schedule.html"'),
        (r'href="schedule-october-17\.html"', 'href="../schedule-october-17.html"'),
        (r'href="schedule-october-18\.html"', 'href="../schedule-october-18.html"'),
        (r'href="speakers\.html"', 'href="../speakers.html"'),
        (r'href="workshops\.html"', 'href="../workshops.html"'),
        (r'href="location\.html"', 'href="../location.html"'),
        (r'href="visa-information\.html"', 'href="../visa-information.html"'),
        (r'href="code-of-conduct\.html"', 'href="../code-of-conduct.html"'),
        (r'href="schedules/', 'href="../schedules/'),
    ]
    
    updated_files = 0
    
    for file_path in speaker_files:
        print(f"Processing: {file_path}")
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all replacements
            for pattern, replacement in url_replacements:
                content = re.sub(pattern, replacement, content)
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files += 1
                print(f"  ✓ Updated: {file_path}")
            else:
                print(f"  - No changes needed: {file_path}")
                
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
    
    print(f"\nSummary: Updated {updated_files} out of {len(speaker_files)} files")

if __name__ == "__main__":
    update_speaker_urls()
