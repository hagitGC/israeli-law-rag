import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
# Correctly import the constant from the constants.py file within the same package
from .constants import LEGISLATION_PORTAL_URL


def extract_legislation_links(portal_url):
    """
    Extracts all unique, relevant links to legislation pages from the Kol Zchut portal page.
    """
    all_links = set()  # Use a set to automatically handle duplicates

    try:
        print(f"Fetching portal page: {portal_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(portal_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='mw-content-text')

        if not content_div:
            print(f"Could not find the main content div ('mw-content-text') on page: {portal_url}")
            return []

        for a_tag in content_div.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') and not href.startswith('//'):
                full_url = urljoin(portal_url, href)
                all_links.add(full_url)

        print(f"Found {len(all_links)} unique links.")
        return sorted(list(all_links))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {portal_url}: {e}")
        return []


if __name__ == "__main__":
    law_links = extract_legislation_links(LEGISLATION_PORTAL_URL)

    if law_links:
        # Save the links to a file in the data directory (relative to project root)
        output_folder = "data"
        output_file = os.path.join(output_folder, "links.txt")

        os.makedirs(output_folder, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            for link in law_links:
                f.write(f"{link}\n")

        print(f"\n--- Successfully saved {len(law_links)} links to {output_file} ---")
    else:
        print("No links were extracted, so no file was created.")
