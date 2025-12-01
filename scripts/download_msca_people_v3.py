"""
Enhanced MSCA People Scraper v3
Downloads photos with proper naming (firstname_lastname.jpg)

Strategy: The Wix page displays person cards with circular photos and names.
We analyze the DOM to find image-name pairs by looking at:
1. Parent containers that hold both image and text
2. Vertical proximity (name text directly below image)
3. Ordered extraction matching visual layout
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

# Institution names to skip (not people)
INSTITUTIONS = {
    'Babes-Bolyai University', 'Bifroest University', 'Cardo AI',
    'Deloitte Consulting', 'Deutsche Bank', 'Deutsche Boerse',
    'European Central Bank', 'Fraunhofer Institute', 'LPA Group',
    'Raiffeisen Bank International AG', 'Sun Yat-sen University',
    'Swedbank AB', 'TED University', 'Athena RC', 'FHGR',
    'University of Twente', 'WU Vienna', 'Kaunas University',
    'Poznan University', 'Quantargo', 'University of Naples',
    'University of Pavia', 'University of Coimbra', 'American University of Sharjah'
}


def sanitize_filename(name):
    """Convert name to safe filename"""
    import unicodedata
    # Remove titles
    name = re.sub(r'^(Prof\.|Dr\.|Mr\.|Ms\.|Mrs\.)\s*', '', name)
    # Normalize unicode characters (e.g., convert accented chars to ASCII)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    # Lowercase and replace spaces with underscores
    safe = re.sub(r'[^\w\s-]', '', name.lower())
    safe = re.sub(r'[\s]+', '_', safe.strip())
    return safe


def download_image(url, filepath):
    """Download image from URL"""
    try:
        # Request higher quality
        download_url = re.sub(r'/v1/fill/w_\d+,h_\d+', '/v1/fill/w_300,h_300', url)

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
    except Exception as e:
        print(f"  Error: {e}")
    return False


def extract_person_cards(page):
    """
    Extract person cards by analyzing DOM structure.
    Returns list of {name, image_url, institution}
    """

    # Wait for full load
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Scroll to load all content
    for _ in range(15):
        page.evaluate('window.scrollBy(0, 600)')
        time.sleep(0.3)
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(2)

    # Extract all elements with their positions
    data = page.evaluate('''() => {
        const results = [];

        // Get all images
        const images = document.querySelectorAll('img');
        const imageData = [];

        images.forEach(img => {
            const src = img.src || '';
            if (src.includes('static.wixstatic.com/media') &&
                !src.includes('logo') &&
                !src.includes('icon')) {
                const rect = img.getBoundingClientRect();
                if (rect.width >= 50 && rect.height >= 50) {
                    imageData.push({
                        src: src,
                        x: rect.left + rect.width/2,
                        y: rect.top + rect.height/2,
                        bottom: rect.bottom
                    });
                }
            }
        });

        // Get all text elements
        const textElements = document.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6, div');
        const textData = [];

        textElements.forEach(el => {
            const text = el.innerText.trim();
            // Filter for name-like text (2-4 words, reasonable length)
            if (text && text.length > 3 && text.length < 60) {
                const words = text.split(/\s+/);
                if (words.length >= 2 && words.length <= 5) {
                    // Check if looks like a name (capitalized words)
                    const looksLikeName = words.every(w =>
                        w.length > 0 && (w[0] === w[0].toUpperCase() || w.length <= 3)
                    );
                    if (looksLikeName) {
                        const rect = el.getBoundingClientRect();
                        textData.push({
                            text: text,
                            x: rect.left + rect.width/2,
                            y: rect.top,
                            top: rect.top
                        });
                    }
                }
            }
        });

        return {images: imageData, texts: textData};
    }''')

    images = data['images']
    texts = data['texts']

    print(f"Found {len(images)} images and {len(texts)} text elements")

    # Match images to names by proximity
    # A name should be close below an image (within 100px horizontally, 10-150px below)

    people = []
    used_texts = set()

    for img in images:
        best_match = None
        best_distance = float('inf')

        for i, txt in enumerate(texts):
            if i in used_texts:
                continue
            if txt['text'] in INSTITUTIONS:
                continue

            # Check if text is below image and horizontally aligned
            dx = abs(txt['x'] - img['x'])
            dy = txt['top'] - img['bottom']  # Should be positive (below)

            if dx < 100 and 5 < dy < 150:
                distance = dx + dy
                if distance < best_distance:
                    best_distance = distance
                    best_match = (i, txt['text'])

        if best_match:
            used_texts.add(best_match[0])
            people.append({
                'name': best_match[1],
                'image_url': img['src']
            })

    return people


def scrape_and_download():
    """Main function"""
    print("MSCA People Scraper v3 - Enhanced Name Matching")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        print(f"Loading {URL}...")
        page.goto(URL, wait_until='networkidle')

        # Extract person cards
        people = extract_person_cards(page)

        browser.close()

    print(f"\nMatched {len(people)} people with images")

    # Download images with proper names
    print("\nDownloading images...")
    print("=" * 60)

    downloaded = []
    seen_names = set()

    for i, person in enumerate(people):
        name = person['name']

        # Skip duplicates
        if name in seen_names:
            continue
        seen_names.add(name)

        # Skip if looks like institution
        if name in INSTITUTIONS:
            continue

        filename = sanitize_filename(name)
        if not filename:
            continue

        # Determine extension
        src = person['image_url']
        ext = '.jpg'
        if '.png' in src:
            ext = '.png'
        elif '.jpeg' in src:
            ext = '.jpeg'

        filepath = ASSETS_DIR / f"{filename}{ext}"

        # Handle Unicode in console output
        try:
            print(f"  [{len(downloaded)+1}] {name} -> {filename}{ext}")
        except UnicodeEncodeError:
            print(f"  [{len(downloaded)+1}] [Unicode name] -> {filename}{ext}")

        if download_image(src, filepath):
            downloaded.append({
                'name': name,
                'filename': f"{filename}{ext}",
                'original_url': src
            })
            print(f"      -> Saved")
        else:
            print(f"      -> FAILED")

    # Save metadata
    metadata = {
        'source_url': URL,
        'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_matched': len(people),
        'downloaded': len(downloaded),
        'people': downloaded
    }

    metadata_path = DATA_DIR / 'msca_people_named.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\nMetadata saved to {metadata_path}")
    print(f"\nSummary:")
    print(f"  - People matched: {len(people)}")
    print(f"  - Images downloaded: {len(downloaded)}")
    print(f"  - Photos saved to: {ASSETS_DIR}")

    # Print downloaded names for verification
    print("\nDownloaded people:")
    for p in downloaded:
        try:
            print(f"  - {p['name']} ({p['filename']})")
        except UnicodeEncodeError:
            print(f"  - [Unicode] ({p['filename']})")

    return downloaded


if __name__ == "__main__":
    scrape_and_download()
