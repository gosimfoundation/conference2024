#!/usr/bin/env python3
"""
Script to remove duplicate speakers from the combined speakers.html file.
Deduplicates based on data-w-id attributes to ensure each speaker appears only once per tab.
"""

from bs4 import BeautifulSoup
import os

def remove_duplicate_speakers():
    """Remove duplicate speakers from the combined speakers.html file."""
    
    # Read the combined speakers.html file
    with open('speakers.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # For each tab, remove duplicates
    for tab_number in range(1, 8):  # Tabs 1-7
        print(f"Processing Tab {tab_number}...")
        
        # Find the tab content
        tab_selector = f'div[data-w-tab="Tab {tab_number}"]'
        tab_content = soup.select_one(tab_selector)
        
        if not tab_content:
            print(f"Tab {tab_number} not found")
            continue
        
        # Find the collection list container
        collection_list = tab_content.select_one('.collection-list.w-dyn-items')
        if not collection_list:
            print(f"Collection list not found in Tab {tab_number}")
            continue
        
        # Get all speaker items
        speaker_items = collection_list.find_all('div', class_='collection-item')
        
        # Track seen data-w-id values
        seen_ids = set()
        duplicates_removed = 0
        
        # Remove duplicates (keep first occurrence)
        for item in speaker_items[:]:  # Create a copy of the list to iterate
            data_w_id = item.get('data-w-id')
            if data_w_id:
                if data_w_id in seen_ids:
                    # This is a duplicate, remove it
                    item.decompose()
                    duplicates_removed += 1
                else:
                    # First time seeing this ID, keep it
                    seen_ids.add(data_w_id)
        
        print(f"Removed {duplicates_removed} duplicates from Tab {tab_number}")
        print(f"Kept {len(seen_ids)} unique speakers in Tab {tab_number}")
    
    # Write the deduplicated file
    with open('speakers_deduplicated.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("Deduplicated speakers file created: speakers_deduplicated.html")

if __name__ == "__main__":
    remove_duplicate_speakers()
