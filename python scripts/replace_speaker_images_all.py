#!/usr/bin/env python3
"""
Comprehensive script to replace speaker image URLs in all HTML files with local image paths.
This script finds all background-image URLs pointing to external CDN and replaces them
with corresponding local image paths from the images/speakers directory.
"""

import os
import re
import urllib.parse
from pathlib import Path
import glob

def extract_filename_from_url(url):
    """Extract the filename from a CDN URL."""
    # Remove the CDN domain and path, keep only the filename
    if '/cdn.prod.website-files.com/' in url:
        # Extract the filename part after the last '/'
        filename = url.split('/')[-1]
        # URL decode the filename
        filename = urllib.parse.unquote(filename)
        return filename
    return None

def find_local_speaker_image(filename):
    """Find the corresponding local speaker image file."""
    speakers_dir = Path("images/speakers")
    if not speakers_dir.exists():
        print(f"Warning: {speakers_dir} directory not found")
        return None
    
    # Look for exact match first
    for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
        potential_file = speakers_dir / filename
        if potential_file.exists():
            return str(potential_file)
    
    # If no exact match, try to find by partial name
    # Remove file extension and try to match
    base_name = Path(filename).stem
    for file_path in speakers_dir.glob("*"):
        if base_name.lower() in file_path.stem.lower():
            return str(file_path)
    
    return None

def replace_speaker_images_in_file(html_file):
    """Replace external speaker image URLs with local paths in a single file."""
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match background-image URLs
    pattern = r'background-image:url\(\.\./cdn\.prod\.website-files\.com/[^)]+\)'
    
    replacements_made = 0
    not_found = []
    
    def replace_url(match):
        nonlocal replacements_made, not_found
        
        url = match.group(0)
        # Extract the URL from the background-image:url(...) syntax
        url_match = re.search(r'url\(([^)]+)\)', url)
        if not url_match:
            return match.group(0)
        
        full_url = url_match.group(1)
        filename = extract_filename_from_url(full_url)
        
        if not filename:
            return match.group(0)
        
        local_path = find_local_speaker_image(filename)
        
        if local_path:
            # Convert to relative path from the HTML file location
            relative_path = os.path.relpath(local_path, os.path.dirname(html_file))
            replacements_made += 1
            print(f"  ✓ Replaced: {filename} -> {relative_path}")
            return f'background-image:url({relative_path})'
        else:
            not_found.append(filename)
            print(f"  ✗ Not found: {filename}")
            return match.group(0)
    
    # Perform the replacement
    new_content = re.sub(pattern, replace_url, content)
    
    # Write the updated content back to the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return replacements_made, not_found

def find_html_files():
    """Find all HTML files in the project."""
    html_files = []
    
    # Find all .html files recursively
    for html_file in glob.glob("**/*.html", recursive=True):
        # Skip any backup or temporary files
        if not any(skip in html_file for skip in ['backup', 'temp', '.bak']):
            html_files.append(html_file)
    
    return html_files

def main():
    """Main function to run the script."""
    print("🔍 Finding all HTML files...")
    html_files = find_html_files()
    
    print(f"Found {len(html_files)} HTML files")
    print("Looking for speaker images in images/speakers/ directory...")
    
    total_replacements = 0
    total_not_found = []
    processed_files = 0
    
    for html_file in html_files:
        print(f"\n📄 Processing: {html_file}")
        
        try:
            replacements, not_found = replace_speaker_images_in_file(html_file)
            
            if replacements > 0:
                print(f"  ✅ Made {replacements} replacements in {html_file}")
                processed_files += 1
            else:
                print(f"  ⚪ No speaker images found in {html_file}")
            
            total_replacements += replacements
            total_not_found.extend(not_found)
            
        except Exception as e:
            print(f"  ❌ Error processing {html_file}: {e}")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY")
    print(f"{'='*50}")
    print(f"Files processed: {processed_files}")
    print(f"Total replacements made: {total_replacements}")
    print(f"Total images not found: {len(set(total_not_found))}")
    
    if total_not_found:
        unique_not_found = list(set(total_not_found))
        print(f"\nImages not found:")
        for filename in unique_not_found:
            print(f"  - {filename}")
    
    if total_replacements > 0:
        print(f"\n✅ Successfully updated {processed_files} files with {total_replacements} local image paths")
    else:
        print(f"\n⚠️  No replacements were made")

if __name__ == "__main__":
    main()
