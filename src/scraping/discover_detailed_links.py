import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time


def discover_links_from_hub_page(hub_url, base_url):
    """
    Visits a single hub page and extracts all relevant internal links from its content.
    """
    detailed_links = set()
    try:
        print(f"  - Scanning hub page: {hub_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(hub_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='mw-content-text')

        if not content_div:
            return set()

        # Find all links within the main content area
        for a_tag in content_div.find_all('a', href=True):
            href = a_tag['href']
            # We only want internal links that are not navigation or file links
            if href.startswith('/') and ':' not in href:
                full_url = urljoin(base_url, href)
                detailed_links.add(full_url)

        return detailed_links

    except requests.exceptions.RequestException as e:
        print(f"    - WARNING: Could not fetch hub URL {hub_url}: {e}")
        return set()


if __name__ == "__main__":
    hub_links_file = "data/links.txt"
    detailed_links_file = "data/detailed_links.txt"
    base_url = "https://www.kolzchut.org.il"  # Needed for urljoin

    if not os.path.exists(hub_links_file):
        print(f"Error: Hub links file '{hub_links_file}' not found.")
        print("Please run 'extract_links.py' first.")
    else:
        with open(hub_links_file, 'r', encoding='utf-8') as f:
            hub_urls = [line.strip() for line in f if line.strip()]

        print(f"--- Found {len(hub_urls)} hub pages to scan. Starting discovery. ---")

        all_detailed_links = set(hub_urls)  # Start with the hub URLs themselves

        for i, url in enumerate(hub_urls):
            discovered_links = discover_links_from_hub_page(url, base_url)
            all_detailed_links.update(discovered_links)
            print(f"  - Progress: {i + 1}/{len(hub_urls)}. Total links found so far: {len(all_detailed_links)}")
            time.sleep(0.5)  # Be polite to the server

        # Save the final, comprehensive list of links
        sorted_links = sorted(list(all_detailed_links))
        os.makedirs("data", exist_ok=True)
        with open(detailed_links_file, 'w', encoding='utf-8') as f:
            for link in sorted_links:
                f.write(f"{link}\n")

        print(f"\n--- Discovery complete. Saved {len(sorted_links)} unique detailed links to {detailed_links_file} ---")
