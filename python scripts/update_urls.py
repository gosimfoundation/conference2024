#!/usr/bin/env python3
"""
Script to update URLs in HTML files to point to local files when possible.
This script will:
1. Find all HTML files in the project
2. Parse each HTML file to find URLs
3. Map external URLs to local files when possible
4. Update the HTML files with local paths
5. List any URLs that don't have corresponding local files
"""

import os
import re
import glob
from pathlib import Path
from urllib.parse import urlparse, unquote
import html
from bs4 import BeautifulSoup
import argparse

class URLUpdater:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.local_files = set()
        self.updated_files = []
        self.missing_files = set()
        self.external_urls = set()
        
        # Build a mapping of external URLs to local files
        self.url_mapping = {}
        
    def scan_local_files(self):
        """Scan all files in the project to build a mapping of external URLs to local files."""
        print("Scanning local files...")
        
        # Find all files in the project
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                self.local_files.add(str(relative_path))
                
                # Also add without extension for potential matches
                stem = relative_path.stem
                self.local_files.add(str(relative_path.parent / stem))
        
        print(f"Found {len(self.local_files)} local files")
        
    def build_url_mapping(self):
        """Build a mapping from external URLs to local file paths."""
        print("Building URL mapping...")
        
        # Common patterns for CDN URLs that might have local equivalents
        cdn_patterns = [
            r'../cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/(.+)',
            r'../d3e54v103j8qbb\.cloudfront\.net/(.+)',
            r'https?://cdn\.prod\.website-files\.com/667a2b77418bcfe1656798ef/(.+)',
            r'https?://d3e54v103j8qbb\.cloudfront\.net/(.+)',
        ]
        
        # Build mapping from external URLs to local files
        for pattern in cdn_patterns:
            for file_path in self.local_files:
                # Extract filename from path
                filename = Path(file_path).name
                
                # Create potential external URL patterns
                potential_urls = [
                    f"../cdn.prod.website-files.com/667a2b77418bcfe1656798ef/{filename}",
                    f"../d3e54v103j8qbb.cloudfront.net/{filename}",
                    f"https://cdn.prod.website-files.com/667a2b77418bcfe1656798ef/{filename}",
                    f"https://d3e54v103j8qbb.cloudfront.net/{filename}",
                ]
                
                for url in potential_urls:
                    self.url_mapping[url] = file_path
        
        # Add specific mappings for common files
        common_mappings = {
            "jquery-3.5.1.min.js": "js/jquery-3.5.1.min.js",
            "china2024.css": "css/china2024.css",
            "china2024.js": "js/china2024.js",
        }
        
        for external_name, local_path in common_mappings.items():
            if local_path in self.local_files:
                self.url_mapping[external_name] = local_path
                self.url_mapping[f"../{external_name}"] = local_path
                self.url_mapping[f"./{external_name}"] = local_path
        
        print(f"Built mapping for {len(self.url_mapping)} URLs")
    
    def find_html_files(self):
        """Find all HTML files in the project."""
        html_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(Path(root) / file)
        return html_files
    
    def extract_urls_from_html(self, html_content):
        """Extract all URLs from HTML content."""
        urls = set()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find URLs in various attributes
        for tag in soup.find_all(['a', 'img', 'link', 'script']):
            # Check href attribute
            if tag.get('href'):
                urls.add(tag['href'])
            
            # Check src attribute
            if tag.get('src'):
                urls.add(tag['src'])
            
            # Check srcset attribute
            if tag.get('srcset'):
                srcset = tag['srcset']
                # Parse srcset to extract URLs
                for item in srcset.split(','):
                    item = item.strip()
                    if item:
                        # Extract URL from srcset item (format: "url width" or just "url")
                        url_part = item.split()[0]
                        urls.add(url_part)
        
        # Also find URLs in inline styles and other attributes
        for tag in soup.find_all():
            for attr_name, attr_value in tag.attrs.items():
                if isinstance(attr_value, str):
                    # Look for URLs in attribute values
                    url_pattern = r'https?://[^\s"\'<>]+'
                    urls.update(re.findall(url_pattern, attr_value))
                    
                    # Look for relative URLs
                    relative_url_pattern = r'\.\./[^\s"\'<>]+'
                    urls.update(re.findall(relative_url_pattern, attr_value))
        
        return urls
    
    def is_external_url(self, url):
        """Check if a URL is external (not a local file)."""
        if not url:
            return False
        
        # Skip anchors, data URLs, and mailto links
        if url.startswith(('#', 'data:', 'mailto:', 'tel:')):
            return False
        
        # Check if it's an absolute URL
        if url.startswith(('http://', 'https://')):
            return True
        
        # Check if it's a relative URL that might be external
        if url.startswith('../'):
            return True
        
        return False
    
    def find_local_file_for_url(self, url):
        """Find a local file that corresponds to the given URL."""
        if not url:
            return None
        
        # Direct mapping
        if url in self.url_mapping:
            return self.url_mapping[url]
        
        # Try to extract filename from URL
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename:
            return None
        
        # Look for exact filename match
        for local_file in self.local_files:
            if Path(local_file).name == filename:
                return local_file
        
        # Try with URL decoding
        decoded_filename = unquote(filename)
        for local_file in self.local_files:
            if Path(local_file).name == decoded_filename:
                return local_file
        
        return None
    
    def update_html_file(self, file_path):
        """Update URLs in a single HTML file."""
        print(f"Processing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return
        
        original_content = content
        urls = self.extract_urls_from_html(content)
        
        # Track changes
        changes_made = False
        file_missing_urls = set()
        file_external_urls = set()
        
        for url in urls:
            if self.is_external_url(url):
                file_external_urls.add(url)
                local_file = self.find_local_file_for_url(url)
                
                if local_file:
                    # Replace the URL with local path
                    # Handle different quote styles
                    patterns = [
                        f'href="{re.escape(url)}"',
                        f"href='{re.escape(url)}'",
                        f'src="{re.escape(url)}"',
                        f"src='{re.escape(url)}'",
                        f'srcset="{re.escape(url)}"',
                        f"srcset='{re.escape(url)}'",
                    ]
                    
                    for pattern in patterns:
                        if re.search(pattern, content):
                            replacement = pattern.replace(url, local_file)
                            content = re.sub(pattern, replacement, content)
                            changes_made = True
                            print(f"  Updated: {url} -> {local_file}")
                else:
                    file_missing_urls.add(url)
        
        # Update the file if changes were made
        if changes_made:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.updated_files.append(str(file_path))
                print(f"  Updated file: {file_path}")
            except Exception as e:
                print(f"Error writing {file_path}: {e}")
        
        # Add missing URLs to global set
        self.missing_files.update(file_missing_urls)
        self.external_urls.update(file_external_urls)
    
    def process_all_files(self):
        """Process all HTML files in the project."""
        print("Processing HTML files...")
        
        html_files = self.find_html_files()
        print(f"Found {len(html_files)} HTML files")
        
        for file_path in html_files:
            self.update_html_file(file_path)
    
    def generate_report(self):
        """Generate a report of the changes made."""
        print("\n" + "="*60)
        print("URL UPDATE REPORT")
        print("="*60)
        
        print(f"\nFiles updated: {len(self.updated_files)}")
        for file in self.updated_files:
            print(f"  - {file}")
        
        print(f"\nExternal URLs found: {len(self.external_urls)}")
        for url in sorted(self.external_urls):
            print(f"  - {url}")
        
        print(f"\nMissing local files: {len(self.missing_files)}")
        for url in sorted(self.missing_files):
            print(f"  - {url}")
        
        # Save report to file
        with open('url_update_report.txt', 'w', encoding='utf-8') as f:
            f.write("URL UPDATE REPORT\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Files updated: {len(self.updated_files)}\n")
            for file in self.updated_files:
                f.write(f"  - {file}\n")
            
            f.write(f"\nExternal URLs found: {len(self.external_urls)}\n")
            for url in sorted(self.external_urls):
                f.write(f"  - {url}\n")
            
            f.write(f"\nMissing local files: {len(self.missing_files)}\n")
            for url in sorted(self.missing_files):
                f.write(f"  - {url}\n")
        
        print(f"\nReport saved to: url_update_report.txt")

def main():
    parser = argparse.ArgumentParser(description='Update URLs in HTML files to point to local files')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--test-file', help='Test on a single file first')
    
    args = parser.parse_args()
    
    updater = URLUpdater(args.project_root)
    
    if args.test_file:
        print(f"Testing on single file: {args.test_file}")
        updater.scan_local_files()
        updater.build_url_mapping()
        updater.update_html_file(Path(args.test_file))
        updater.generate_report()
    else:
        print("Processing all HTML files...")
        updater.scan_local_files()
        updater.build_url_mapping()
        updater.process_all_files()
        updater.generate_report()

if __name__ == "__main__":
    main()
