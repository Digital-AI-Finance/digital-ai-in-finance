"""
Download all people photos and bios from MSCA Digital Finance website
https://www.digital-finance-msca.com/our-people

Uses Playwright for JavaScript-rendered content extraction.
"""

import json
import re
import requests
import time
from pathlib import Path
from urllib.parse import urljoin

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
    # Remove special characters, replace spaces with underscores
    safe = re.sub(r'[^\w\s-]', '', name.lower())
    safe = re.sub(r'[\s]+', '_', safe)
    return safe


def download_image(url, filepath):
    """Download image from URL to filepath"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
    return False


def extract_people_from_page(page):
    """Extract all people data from the rendered page"""
    people = []

    # Wait for content to load
    page.wait_for_load_state("networkidle")
    time.sleep(3)  # Extra wait for dynamic content

    # Try different selectors that Wix might use
    # Wix often uses data-testid or specific class patterns

    # First, let's get all the content and debug
    content = page.content()

    # Look for image elements with person photos
    # Wix typically uses wixui-image or specific patterns

    # Try to find person cards/sections
    selectors_to_try = [
        '[data-testid*="richTextElement"]',
        '[data-testid*="image"]',
        '.font_8',  # Common Wix text class
        '[class*="rich-text"]',
        'img[src*="wix"]',
        '[class*="comp-"]',  # Wix component class
    ]

    # Get all images
    images = page.query_selector_all('img')
    print(f"Found {len(images)} total images on page")

    # Filter for person photos (usually larger images, not icons)
    person_images = []
    for img in images:
        src = img.get_attribute('src') or ''
        alt = img.get_attribute('alt') or ''

        # Skip small icons, logos, etc.
        if 'logo' in src.lower() or 'icon' in src.lower():
            continue
        if 'static.wixstatic.com/media' in src:
            # Get image dimensions if possible
            width = img.get_attribute('width')
            height = img.get_attribute('height')

            # This looks like a content image
            person_images.append({
                'src': src,
                'alt': alt,
                'width': width,
                'height': height
            })

    print(f"Found {len(person_images)} potential person images")

    # Get all text blocks that might contain names/bios
    text_elements = page.query_selector_all('p, h1, h2, h3, h4, h5, h6, span, div')

    # Look for patterns like "Prof. Name" or "Dr. Name"
    name_pattern = re.compile(r'^(Prof\.|Dr\.|Mr\.|Ms\.|Mrs\.)\s+[\w\s]+$|^[\w]+\s+[\w]+$')

    texts = []
    for elem in text_elements:
        text = elem.inner_text().strip()
        if text and len(text) > 2 and len(text) < 200:
            texts.append(text)

    # Remove duplicates while preserving order
    seen = set()
    unique_texts = []
    for t in texts:
        if t not in seen:
            seen.add(t)
            unique_texts.append(t)

    print(f"Found {len(unique_texts)} unique text elements")

    # Save raw data for debugging
    debug_data = {
        'images': person_images,
        'texts': unique_texts[:100]  # First 100 texts
    }

    with open(DATA_DIR / 'msca_raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(debug_data, f, indent=2, ensure_ascii=False)

    print(f"Raw data saved to {DATA_DIR / 'msca_raw_data.json'}")

    return person_images, unique_texts


def scrape_msca_people():
    """Main scraping function"""
    print(f"Scraping {URL}")
    print("=" * 60)

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        # Navigate to page
        print("Loading page...")
        page.goto(URL, wait_until='networkidle')

        # Scroll to load lazy content
        print("Scrolling to load all content...")
        for _ in range(5):
            page.evaluate('window.scrollBy(0, 1000)')
            time.sleep(0.5)
        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(2)

        # Take screenshot for debugging
        screenshot_path = DATA_DIR / 'msca_page_screenshot.png'
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        # Extract data
        images, texts = extract_people_from_page(page)

        browser.close()

    return images, texts


def download_all_images(images):
    """Download all person images"""
    print("\nDownloading images...")
    print("=" * 60)

    downloaded = []
    for i, img in enumerate(images):
        src = img.get('src', '')
        if not src:
            continue

        # Clean up Wix image URL (remove resize parameters for full quality)
        if 'wixstatic.com' in src:
            # Get base image URL
            base_url = src.split('/v1/')[0] if '/v1/' in src else src
            if '/v1/' in src:
                # Extract file part
                parts = src.split('/v1/')
                if len(parts) > 1:
                    file_part = parts[1].split('/')[0]
                    src = f"{parts[0]}/v1/{file_part}"

        filename = f"person_{i+1:02d}.jpg"
        filepath = ASSETS_DIR / filename

        print(f"  [{i+1}/{len(images)}] Downloading {filename}...")

        if download_image(src, filepath):
            downloaded.append({
                'index': i + 1,
                'filename': filename,
                'original_url': img.get('src'),
                'alt': img.get('alt', '')
            })
            print(f"    -> Saved to {filepath}")
        else:
            print(f"    -> FAILED")

    return downloaded


def main():
    print("MSCA Digital Finance - People Scraper")
    print("=" * 60)

    # Scrape the page
    images, texts = scrape_msca_people()

    # Download all images
    downloaded = download_all_images(images)

    # Save metadata
    metadata = {
        'source_url': URL,
        'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_images': len(images),
        'downloaded_images': len(downloaded),
        'images': downloaded,
        'extracted_texts': texts[:50]  # Save first 50 text snippets
    }

    metadata_path = DATA_DIR / 'msca_people.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\nMetadata saved to {metadata_path}")
    print(f"\nSummary:")
    print(f"  - Total images found: {len(images)}")
    print(f"  - Images downloaded: {len(downloaded)}")
    print(f"  - Text snippets extracted: {len(texts)}")

    print("\n" + "=" * 60)
    print("NEXT STEP: Run select_committee.py to choose Scientific Committee members")
    print("=" * 60)


if __name__ == "__main__":
    main()
