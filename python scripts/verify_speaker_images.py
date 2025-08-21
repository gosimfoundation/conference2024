#!/usr/bin/env python3
"""
Verification script to check if all speaker images have been successfully replaced with local paths.
This script scans HTML files to ensure no external CDN URLs remain for speaker images.
"""

import re
import glob
from pathlib import Path

def check_html_file(html_file):
    """Check a single HTML file for remaining external speaker image URLs."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match background-image URLs pointing to external CDN
    pattern = r'background-image:url\(\.\./cdn\.prod\.website-files\.com/[^)]+\)'
    
    matches = re.findall(pattern, content)
    
    if matches:
        print(f"❌ {html_file}: {len(matches)} external URLs found")
        for match in matches:
            print(f"    - {match}")
        return False
    else:
        print(f"✅ {html_file}: No external URLs found")
        return True

def main():
    """Main function to verify speaker image replacements."""
    print("🔍 Verifying speaker image replacements...")
    print("Checking for any remaining external CDN URLs...")
    
    # Find all HTML files
    html_files = []
    for html_file in glob.glob("**/*.html", recursive=True):
        if not any(skip in html_file for skip in ['backup', 'temp', '.bak']):
            html_files.append(html_file)
    
    print(f"\nFound {len(html_files)} HTML files to check")
    
    all_clean = True
    files_with_issues = []
    
    for html_file in html_files:
        if not check_html_file(html_file):
            all_clean = False
            files_with_issues.append(html_file)
    
    print(f"\n{'='*50}")
    print(f"📊 VERIFICATION SUMMARY")
    print(f"{'='*50}")
    
    if all_clean:
        print("✅ All files are clean! No external speaker image URLs found.")
    else:
        print(f"❌ Found issues in {len(files_with_issues)} files:")
        for file in files_with_issues:
            print(f"  - {file}")
    
    # Also check if local images exist
    print(f"\n🔍 Checking local speaker images...")
    speakers_dir = Path("images/speakers")
    if speakers_dir.exists():
        image_count = len(list(speakers_dir.glob("*")))
        print(f"✅ Found {image_count} speaker images in {speakers_dir}")
    else:
        print(f"❌ Speaker images directory not found: {speakers_dir}")

if __name__ == "__main__":
    main()
