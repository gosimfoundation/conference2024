#!/usr/bin/env python3
"""
Script to update all URLs in CSS file to point to local project assets.
This script will:
1. Find all external URLs in the CSS file
2. Check if corresponding assets exist in the images directory
3. Replace external URLs with local relative paths
4. Keep track of assets that couldn't be updated
"""

import os
import re
import urllib.parse
from pathlib import Path

def extract_filename_from_url(url):
    """Extract filename from URL, handling URL encoding."""
    # Remove query parameters and fragments
    url = url.split('?')[0].split('#')[0]
    
    # Get the filename from the URL
    filename = os.path.basename(url)
    
    # URL decode the filename
    try:
        filename = urllib.parse.unquote(filename)
    except:
        pass
    
    return filename

def find_asset_in_images(filename, images_dir):
    """Find an asset in the images directory, trying different variations."""
    # Direct match
    if os.path.exists(os.path.join(images_dir, filename)):
        return filename
    
    # Try without URL encoding
    decoded_filename = urllib.parse.unquote(filename)
    if os.path.exists(os.path.join(images_dir, decoded_filename)):
        return decoded_filename
    
    # Try common variations
    variations = [
        filename,
        decoded_filename,
        filename.replace('%20', ' '),
        filename.replace('%2C', ','),
        filename.replace('%2F', '/'),
        filename.replace('%3A', ':'),
        filename.replace('%40', '@'),
    ]
    
    for variation in variations:
        if os.path.exists(os.path.join(images_dir, variation)):
            return variation
    
    return None

def update_css_urls(css_file_path, images_dir):
    """Update URLs in CSS file to point to local assets."""
    
    # Read the CSS file
    with open(css_file_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Patterns to match different types of URLs
    url_patterns = [
        # background-image: url("https://...")
        r'background-image:\s*url\(["\']?(https://[^"\']+)["\']?\)',
        # src: url('https://...')
        r'src:\s*url\(["\']?(https://[^"\']+)["\']?\)',
        # Any other url("https://...")
        r'url\(["\']?(https://[^"\']+)["\']?\)',
    ]
    
    updated_count = 0
    failed_assets = []
    
    # Process each pattern
    for pattern in url_patterns:
        matches = re.finditer(pattern, css_content, re.IGNORECASE)
        
        for match in matches:
            original_url = match.group(1)
            filename = extract_filename_from_url(original_url)
            
            # Skip data URLs
            if filename.startswith('data:'):
                continue
            
            # Find the asset in images directory
            found_asset = find_asset_in_images(filename, images_dir)
            
            if found_asset:
                # Create relative path from CSS file to images directory
                css_dir = os.path.dirname(css_file_path)
                relative_path = os.path.relpath(os.path.join(images_dir, found_asset), css_dir)
                
                # Replace the URL
                new_url = f'url("../{found_asset}")'
                css_content = css_content.replace(match.group(0), new_url)
                updated_count += 1
                print(f"Updated: {original_url} -> {new_url}")
            else:
                failed_assets.append({
                    'url': original_url,
                    'filename': filename,
                    'context': match.group(0)
                })
                print(f"Failed to find asset: {filename}")
    
    # Write the updated CSS content
    with open(css_file_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    return updated_count, failed_assets

def main():
    # File paths
    css_file = "css/china2024.css"
    images_dir = "images"
    
    # Check if files exist
    if not os.path.exists(css_file):
        print(f"Error: CSS file '{css_file}' not found")
        return
    
    if not os.path.exists(images_dir):
        print(f"Error: Images directory '{images_dir}' not found")
        return
    
    print(f"Updating URLs in {css_file}...")
    print(f"Looking for assets in {images_dir}...")
    print("-" * 50)
    
    # Update the URLs
    updated_count, failed_assets = update_css_urls(css_file, images_dir)
    
    # Print summary
    print("-" * 50)
    print(f"Update complete!")
    print(f"Successfully updated: {updated_count} URLs")
    print(f"Failed to update: {len(failed_assets)} URLs")
    
    # Print failed assets
    if failed_assets:
        print("\nAssets that could not be updated:")
        print("=" * 50)
        for asset in failed_assets:
            print(f"URL: {asset['url']}")
            print(f"Filename: {asset['filename']}")
            print(f"Context: {asset['context']}")
            print("-" * 30)
    
    # Save failed assets to a file
    if failed_assets:
        with open("failed_assets_report.txt", "w", encoding="utf-8") as f:
            f.write("Assets that could not be updated:\n")
            f.write("=" * 50 + "\n")
            for asset in failed_assets:
                f.write(f"URL: {asset['url']}\n")
                f.write(f"Filename: {asset['filename']}\n")
                f.write(f"Context: {asset['context']}\n")
                f.write("-" * 30 + "\n")
        print(f"\nFailed assets report saved to: failed_assets_report.txt")

if __name__ == "__main__":
    main()
