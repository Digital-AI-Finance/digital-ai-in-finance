"""
Download all people photos from MSCA Digital Finance website (v2)
https://www.digital-finance-msca.com/our-people

Improved version that:
1. Downloads unique images only
2. Converts AVIF URLs to JPEG for compatibility
3. Saves proper metadata with names
"""

import json
import re
import requests
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "playwright"])
    subprocess.run(["playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://www.digital-finance-msca.com/our-people"


def sanitize_filename(name):
    """Convert name to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', name.lower())
    safe = re.sub(r'[\s]+', '_', safe)
    return safe


def convert_wix_url_to_jpeg(url):
    """Convert Wix AVIF URL to JPEG format for better compatibility"""
    # Remove AVIF encoding and quality parameters, request JPEG
    if 'enc_avif' in url or 'enc_auto' in url:
        # Replace encoding with JPEG
        url = re.sub(r',enc_\w+', ',enc_auto', url)

    # For better quality, modify the fill parameters
    # Change small thumbnails to larger images
    url = re.sub(r'/v1/fill/w_\d+,h_\d+', '/v1/fill/w_300,h_300', url)

    return url


def download_image(url, filepath):
    """Download image from URL to filepath"""
    try:
        # Convert URL for better format
        download_url = convert_wix_url_to_jpeg(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://www.digital-finance-msca.com/'
        }

        response = requests.get(download_url, timeout=30, headers=headers)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"  HTTP {response.status_code} for {download_url[:60]}...")
    except Exception as e:
        print(f"  Error downloading: {e}")
    return False


def extract_people_data(page):
    """Extract structured people data from the page"""

    # Wait for content
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Scroll to load lazy content
    for _ in range(10):
        page.evaluate('window.scrollBy(0, 800)')
        time.sleep(0.3)
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(2)

    # Get all unique images (filter by size - person photos are typically 159x159)
    images = page.query_selector_all('img')

    person_images = {}  # Use dict to dedupe by URL
    for img in images:
        src = img.get_attribute('src') or ''
        if not src or 'static.wixstatic.com/media' not in src:
            continue

        # Skip small icons (logos, social icons)
        width = img.get_attribute('width')
        height = img.get_attribute('height')

        try:
            w = int(width) if width else 0
            h = int(height) if height else 0
        except:
            w, h = 0, 0

        # Person photos are typically 159x159 or similar square format
        if w >= 45 and h >= 45:  # Allow some variation
            # Extract unique identifier from URL
            match = re.search(r'media/([^/]+)~mv2', src)
            if match:
                img_id = match.group(1)
                if img_id not in person_images:
                    person_images[img_id] = {
                        'id': img_id,
                        'src': src,
                        'alt': img.get_attribute('alt') or '',
                        'width': w,
                        'height': h
                    }

    # Get text elements that look like names
    all_text = page.evaluate('''() => {
        const texts = [];
        document.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6').forEach(el => {
            const text = el.innerText.trim();
            if (text && text.length > 1 && text.length < 100) {
                texts.push(text);
            }
        });
        return texts;
    }''')

    # Filter for name-like entries
    names = []
    seen = set()
    for t in all_text:
        if t in seen:
            continue
        seen.add(t)

        # Skip menu items and common headers
        skip_words = ['Research', 'About', 'Partners', 'People', 'Governance',
                      'Diversity', 'Outputs', 'Positions', 'Contact', 'Privacy',
                      'Area', 'Topics', 'Our ', 'Open ', 'More']
        if any(skip in t for skip in skip_words):
            continue

        # Keep entries that look like names (2-4 words, title case)
        words = t.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
            names.append(t)

    return list(person_images.values()), names


def scrape_msca_people():
    """Main scraping function"""
    print(f"Scraping {URL}")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        print("Loading page...")
        page.goto(URL, wait_until='networkidle')

        # Extract data
        images, names = extract_people_data(page)

        browser.close()

    print(f"Found {len(images)} unique person images")
    print(f"Found {len(names)} potential names")

    return images, names


def download_all_images(images):
    """Download all unique person images"""
    print("\nDownloading images...")
    print("=" * 60)

    downloaded = []
    for i, img in enumerate(images):
        src = img.get('src', '')
        if not src:
            continue

        # Determine file extension
        ext = '.jpg'
        if '.png' in src:
            ext = '.png'
        elif '.jpeg' in src:
            ext = '.jpeg'

        filename = f"person_{i+1:02d}{ext}"
        filepath = ASSETS_DIR / filename

        print(f"  [{i+1}/{len(images)}] Downloading {filename}...")

        if download_image(src, filepath):
            downloaded.append({
                'index': i + 1,
                'filename': filename,
                'original_url': src,
                'img_id': img.get('id', ''),
                'alt': img.get('alt', '')
            })
            print(f"    -> Saved")
        else:
            print(f"    -> FAILED")

    return downloaded


def main():
    print("MSCA Digital Finance - People Scraper v2")
    print("=" * 60)

    # Scrape the page
    images, names = scrape_msca_people()

    # Download all images
    downloaded = download_all_images(images)

    # Save metadata
    metadata = {
        'source_url': URL,
        'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_unique_images': len(images),
        'downloaded_images': len(downloaded),
        'potential_names': names,
        'images': downloaded
    }

    metadata_path = DATA_DIR / 'msca_people.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\nMetadata saved to {metadata_path}")
    print(f"\nSummary:")
    print(f"  - Unique images found: {len(images)}")
    print(f"  - Images downloaded: {len(downloaded)}")
    print(f"  - Names extracted: {len(names)}")

    if downloaded:
        print(f"\nImages saved to: {ASSETS_DIR}")

    print("\n" + "=" * 60)
    print("NEXT STEP: Run select_committee.py to choose Scientific Committee members")
    print("=" * 60)


if __name__ == "__main__":
    main()
