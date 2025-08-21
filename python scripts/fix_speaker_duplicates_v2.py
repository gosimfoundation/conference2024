#!/usr/bin/env python3
"""
Script to remove duplicate speakers from the combined speakers.html file.
Deduplicates based on speaker names to ensure each speaker appears only once per tab.
"""

from bs4 import BeautifulSoup
import os

def get_speaker_name(speaker_item):
    """Extract the speaker name from a speaker item."""
    heading = speaker_item.find('h3', class_='heading')
    if heading:
        return heading.get_text(strip=True)
    return None

def remove_duplicate_speakers_by_name():
    """Remove duplicate speakers from the combined speakers.html file based on names."""
    
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
        
        # Track seen speaker names
        seen_names = set()
        duplicates_removed = 0
        
        # Remove duplicates (keep first occurrence)
        for item in speaker_items[:]:  # Create a copy of the list to iterate
            speaker_name = get_speaker_name(item)
            if speaker_name:
                if speaker_name in seen_names:
                    # This is a duplicate, remove it
                    item.decompose()
                    duplicates_removed += 1
                else:
                    # First time seeing this name, keep it
                    seen_names.add(speaker_name)
        
        print(f"Removed {duplicates_removed} duplicates from Tab {tab_number}")
        print(f"Kept {len(seen_names)} unique speakers in Tab {tab_number}")
        
        # Print some example names for verification
        if seen_names:
            print(f"Sample speakers in Tab {tab_number}: {list(seen_names)[:3]}")
    
    # Write the deduplicated file
    with open('speakers_deduplicated_v2.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("Deduplicated speakers file created: speakers_deduplicated_v2.html")

if __name__ == "__main__":
    remove_duplicate_speakers_by_name()
