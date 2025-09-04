import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_legislation_links(portal_url):
    """
    Extracts all unique, relevant links to legislation pages from the Kol Zchut portal page.
    """
    all_links = set()  # Using a set to automatically handle duplicates

    try:
        print(f"Fetching portal page: {portal_url}")
        # Using headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(portal_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- THIS IS THE CORRECTED LINE ---
        # Based on the provided HTML, the correct container ID is 'mw-content-text'.
        content_div = soup.find('div', id='mw-content-text')

        if not content_div:
            print(f"Could not find the main content div ('mw-content-text') on page: {portal_url}")
            return []

        # Find all <a> (anchor/link) tags within the content div
        for a_tag in content_div.find_all('a', href=True):
            href = a_tag['href']

            # We only want internal links to law pages, not external links (like to nevo.co.il)
            # or section links (#)
            if href.startswith('/') and not href.startswith('//'):
                full_url = urljoin(portal_url, href)
                all_links.add(full_url)

        print(f"Found {len(all_links)} unique links.")
        return sorted(list(all_links))  # Return a sorted list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {portal_url}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# --- Main script execution ---
if __name__ == "__main__":
    # The main page that lists all the laws and procedures
    LEGISLATION_PORTAL_URL = "https://www.kolzchut.org.il/he/%D7%AA%D7%A2%D7%A1%D7%95%D7%A7%D7%94_%D7%95%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA_%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D/%D7%97%D7%A7%D7%99%D7%A7%D7%94_%D7%95%D7%A0%D7%94%D7%9C%D7%99%D7%9D"

    # Get the list of all law page URLs
    law_links = extract_legislation_links(LEGISLATION_PORTAL_URL)

    # Print the extracted links
    if law_links:
        print("\n--- Extracted Links ---")
        for link in law_links:
            print(link)
    else:
        print("No links were extracted.")

