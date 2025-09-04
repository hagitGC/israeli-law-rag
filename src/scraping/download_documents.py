import requests
from bs4 import BeautifulSoup
import os
import time
import argparse


def download_and_save_page(url, output_folder="data/raw"):
    """
    Fetches content from a Kol Zchut page, cleans out irrelevant sections,
    extracts the page title for the filename, and saves the core text to a file.
    """
    try:
        print(f"Downloading: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='mw-content-text')

        # --- NEW: Extract the main title for a better filename ---
        page_title_tag = soup.find('h1', id='firstHeading')
        if page_title_tag and page_title_tag.get_text(strip=True):
            page_title = page_title_tag.get_text(strip=True)
        else:
            # Fallback to the URL slug if title tag is not found
            page_title = url.strip().split('/')[-1]

        # Clean the title to create a valid filename
        invalid_chars = r'<>:"/\|?*'
        filename = "".join(c if c not in invalid_chars else '_' for c in page_title).rstrip()
        # --- END NEW FILENAME LOGIC ---

        if not content_div:
            print(f"  - WARNING: Could not find content for {url}. Skipping.")
            return

        # Clean the HTML before extracting text
        elements_to_remove = [
            {'name': 'div', 'class_': 'toc-box'},
            {'name': 'div', 'id': 'chat-section'},
            {'name': 'div', 'class_': 'wr-infobox-nuevo-wrapper'}
        ]
        for selector in elements_to_remove:
            for tag in content_div.find_all(selector.get('name'), class_=selector.get('class_'), id=selector.get('id')):
                tag.decompose()

        page_text = content_div.get_text(separator='\n', strip=True)

        if not filename:
            filename = f"document_{hash(url)}"

        output_filepath = os.path.join(output_folder, f"{filename}.txt")
        os.makedirs(output_folder, exist_ok=True)

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(page_text)

        print(f"  - Saved cleaned content to: {output_filepath}")

    except requests.exceptions.RequestException as e:
        print(f"  - ERROR: Could not fetch URL {url}: {e}")
    except Exception as e:
        print(f"  - ERROR: An unexpected error occurred for {url}: {e}")


if __name__ == "__main__":
    # Setup argument parser to allow controlling the number of downloads
    parser = argparse.ArgumentParser(description="Download law documents from Kol Zchut based on a list of URLs.")
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=None,
        help="Limit the number of documents to download (e.g., for testing)."
    )
    args = parser.parse_args()

    links_file = "data/detailed_links.txt"

    if not os.path.exists(links_file):
        print(f"Error: The detailed links file '{links_file}' was not found.")
        print("Please run 'discover_detailed_links.py' first to generate it.")
    else:
        with open(links_file, 'r', encoding='utf-8') as f:
            urls_to_download = [line.strip() for line in f if line.strip()]

        # Apply the limit if the user provided one
        if args.limit and args.limit > 0:
            print(f"--- Limiting download to the first {args.limit} documents. ---")
            urls_to_download = urls_to_download[:args.limit]

        print(f"--- Found {len(urls_to_download)} detailed URLs to download. Starting process. ---")

        for i, url in enumerate(urls_to_download):
            download_and_save_page(url)
            time.sleep(1)
            print(f"  - Progress: {i + 1}/{len(urls_to_download)}")

        print("\n--- Download process complete. ---")

