#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests",
# ]
# ///
"""
Script to fetch all tables from SCB API with pagination.
Paces requests to avoid firewalls (1 request every 2 seconds).
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "https://statistikdatabasen.scb.se/api/v2/tables"
PAGE_SIZE = 20  # Default page size from API spec
DELAY_SECONDS = 2  # Delay between requests to avoid firewalls

def fetch_page(page_number):
    """Fetch a single page of tables from the API."""
    params = {
        'pageNumber': page_number,
        'pageSize': PAGE_SIZE
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return None

def save_page_data(page_data, page_number):
    """Save page data to a file."""
    output_dir = Path("tables")
    output_dir.mkdir(exist_ok=True)
    
    filename = output_dir / f"page_{page_number}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(page_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved page {page_number} with {len(page_data['tables'])} tables to {filename}")

def main():
    # First fetch to get total pages
    first_page = fetch_page(1)
    if not first_page:
        print("Failed to fetch first page")
        return
    
    total_pages = first_page['page']['totalPages']
    print(f"Total pages available: {total_pages}")
    
    # Fetch ALL pages to document all 5155 tables
    max_pages_to_fetch = total_pages  # Fetch ALL pages
    print(f"Fetching ALL {max_pages_to_fetch} pages to document all tables...")
    print(f"This will take approximately {max_pages_to_fetch * DELAY_SECONDS / 60:.1f} minutes")
    
    # Save first page
    save_page_data(first_page, 1)
    
    # Fetch remaining pages with delay
    for page in range(2, max_pages_to_fetch + 1):
        print(f"Waiting {DELAY_SECONDS} seconds before fetching page {page}...")
        time.sleep(DELAY_SECONDS)
        
        page_data = fetch_page(page)
        if page_data:
            save_page_data(page_data, page)
        else:
            print(f"Skipping page {page} due to error")
    
    print(f"Completed fetching ALL {max_pages_to_fetch} pages")
    print(f"Total tables documented: {total_pages * PAGE_SIZE}")

if __name__ == "__main__":
    main()