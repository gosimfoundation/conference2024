#!/usr/bin/env python3
"""
Script to fix the double quotes issue in CSS URLs
"""

import re

def fix_css_urls():
    css_file = 'css/china2024.css'
    
    # Read the CSS file
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix double quotes in background-image URLs
    content = re.sub(r'url\("\'([^\']+)\'"\)', r'url("\1")', content)
    
    # Fix double quotes in font src URLs
    content = re.sub(r"url\(''([^']+)''\)", r"url('\1')", content)
    
    # Write the corrected content back to the file
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed double quotes in CSS URLs")

if __name__ == "__main__":
    fix_css_urls()
