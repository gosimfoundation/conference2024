#!/usr/bin/env python3
"""
Script to replace speaker image URLs in speakers.html with local image paths.
This script finds all background-image URLs pointing to external CDN and replaces them
with corresponding local image paths from the images/speakers directory.
"""

import os
import re
import urllib.parse
from pathlib import Path

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

def replace_speaker_images(html_file):
    """Replace external speaker image URLs with local paths."""
    
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
            print(f"✓ Replaced: {filename} -> {relative_path}")
            return f'background-image:url({relative_path})'
        else:
            not_found.append(filename)
            print(f"✗ Not found: {filename}")
            return match.group(0)
    
    # Perform the replacement
    new_content = re.sub(pattern, replace_url, content)
    
    # Write the updated content back to the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total replacements made: {replacements_made}")
    print(f"Images not found: {len(not_found)}")
    
    if not_found:
        print(f"\nImages not found:")
        for filename in not_found:
            print(f"  - {filename}")
    
    return replacements_made, not_found

def main():
    """Main function to run the script."""
    html_file = "speakers.html"
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found")
        return
    
    print(f"Processing {html_file}...")
    print("Looking for speaker images in images/speakers/ directory...")
    
    replacements, not_found = replace_speaker_images(html_file)
    
    if replacements > 0:
        print(f"\n✅ Successfully updated {html_file} with {replacements} local image paths")
    else:
        print(f"\n⚠️  No replacements were made")

if __name__ == "__main__":
    main()
