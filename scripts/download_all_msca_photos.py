"""
Download ALL photos from MSCA Digital Finance website
Comprehensive scraper that captures every person's photo
"""

import json
import re
import time
import requests
import unicodedata
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"
DATA_DIR = BASE_DIR / "data"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    """Convert name to safe filename"""
    name = re.sub(r'^(Prof\.|Dr\.|Mr\.|Ms\.|Mrs\.)\s*', '', name)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    safe = re.sub(r'[^\w\s-]', '', name.lower())
    safe = re.sub(r'[\s]+', '_', safe.strip())
    return safe

def download_image(url, filepath):
    """Download image and return success, size"""
    try:
        # Get higher resolution version
        url = re.sub(r'/w_\d+,h_\d+', '/w_400,h_400', url)
        url = re.sub(r'fill/w_\d+,h_\d+', 'fill/w_400,h_400', url)

        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 2000:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            return True, len(resp.content)
    except Exception as e:
        pass
    return False, 0

def scrape_all_photos():
    """Scrape all photos with their associated names"""

    print("Launching browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading MSCA Our People page...")
        page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        time.sleep(4)

        # Scroll extensively to load all lazy-loaded images
        print("Scrolling to load all content...")
        page_height = page.evaluate("document.body.scrollHeight")

        for i in range(30):
            page.evaluate(f"window.scrollTo(0, {i * 400})")
            time.sleep(0.25)

        # Scroll back up
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        # Scroll down again slowly
        for i in range(40):
            page.evaluate(f"window.scrollTo(0, {i * 300})")
            time.sleep(0.15)

        print("Extracting all person data...")

        # Extract all person cards with images and names
        people_data = page.evaluate(r'''() => {
            const people = [];
            const processedImages = new Set();

            // Get all images
            const allImages = document.querySelectorAll('img');

            allImages.forEach(img => {
                const src = img.src || img.dataset.src || '';
                if (!src) return;
                if (!src.includes('wixstatic.com')) return;
                if (processedImages.has(src)) return;

                // Skip very small images (icons)
                const rect = img.getBoundingClientRect();
                if (rect.width < 40 || rect.height < 40) return;

                processedImages.add(src);

                // Find the name associated with this image
                // Look in parent containers for text that looks like a name
                let name = '';
                let container = img.parentElement;

                for (let level = 0; level < 6 && container; level++) {
                    // Look for text elements
                    const textElements = container.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6');

                    for (const el of textElements) {
                        if (el.contains(img)) continue; // Skip if contains the image

                        const text = el.innerText.trim();
                        if (!text || text.length < 4 || text.length > 50) continue;

                        // Check if it looks like a person's name
                        const words = text.split(/\s+/);
                        if (words.length < 2 || words.length > 5) continue;

                        // Must start with capital letters
                        const looksLikeName = words.every(w => /^[A-Z]/.test(w));
                        if (!looksLikeName) continue;

                        // Skip institution names
                        if (/University|Institute|Center|School|Department|Research|European|Horizon/i.test(text)) continue;

                        // Skip dates and common non-name patterns
                        if (/^\d|January|February|March|April|May|June|July|August|September|October|November|December/i.test(text)) continue;

                        name = text;
                        break;
                    }

                    if (name) break;
                    container = container.parentElement;
                }

                if (name) {
                    people.push({
                        name: name,
                        imageUrl: src,
                        width: rect.width,
                        height: rect.height
                    });
                }
            });

            return people;
        }''')

        print(f"Found {len(people_data)} people with images")

        browser.close()
        return people_data

def main():
    print("=" * 60)
    print("MSCA Digital Finance - Complete Photo Downloader")
    print("=" * 60)

    # Load committee members
    with open(DATA_DIR / "scientific_committee.json", 'r') as f:
        committee = json.load(f)['selected']

    committee_lower = {sanitize_filename(c): c for c in committee}

    # Scrape all photos
    people = scrape_all_photos()

    # Download all photos
    print("\nDownloading photos...")
    downloaded = {}

    for person in people:
        name = person['name']
        url = person['imageUrl']

        filename = sanitize_filename(name)
        if not filename:
            continue

        # Determine extension
        ext = '.png' if '.png' in url.lower() else '.jpg'
        filepath = ASSETS_DIR / (filename + ext)

        # Skip if already have a good version
        if filepath.exists() and filepath.stat().st_size > 5000:
            downloaded[name] = {'filename': filename + ext, 'size': filepath.stat().st_size}
            continue

        success, size = download_image(url, filepath)
        if success:
            downloaded[name] = {'filename': filename + ext, 'size': size}
            try:
                print(f"  Downloaded: {name} ({size/1024:.1f} KB)")
            except:
                print(f"  Downloaded: [name] ({size/1024:.1f} KB)")

    print(f"\nTotal downloaded/existing: {len(downloaded)}")

    # Check committee coverage
    print("\n" + "=" * 60)
    print("Committee Member Photo Status:")
    print("=" * 60)

    found = 0
    missing = []

    for member in committee:
        member_fn = sanitize_filename(member)

        # Check for photo file
        has_photo = False
        for ext in ['.jpg', '.png']:
            fpath = ASSETS_DIR / (member_fn + ext)
            if fpath.exists() and fpath.stat().st_size > 3000:
                has_photo = True
                found += 1
                try:
                    print(f"  [OK] {member}")
                except:
                    print(f"  [OK] [member name]")
                break

        if not has_photo:
            missing.append(member)
            try:
                print(f"  [MISSING] {member}")
            except:
                print(f"  [MISSING] [member name]")

    print(f"\nCommittee photos: {found}/{len(committee)}")

    if missing:
        print(f"\nMissing {len(missing)} members - these may not have photos on MSCA:")
        for m in missing:
            try:
                print(f"  - {m}")
            except:
                print(f"  - [name]")

    # Update mappings file
    mappings = {'people': [], 'source': 'https://www.digital-finance-msca.com/our-people'}

    for fpath in ASSETS_DIR.glob('*.*'):
        if fpath.suffix.lower() in ['.jpg', '.png'] and fpath.stat().st_size > 3000:
            name_parts = fpath.stem.replace('_', ' ').replace('-', ' ').title().split()
            name = ' '.join(name_parts)
            mappings['people'].append({
                'name': name,
                'filename': fpath.name,
                'size': fpath.stat().st_size
            })

    with open(DATA_DIR / 'msca_people_named.json', 'w') as f:
        json.dump(mappings, f, indent=2)

    print(f"\nUpdated mappings: {len(mappings['people'])} people with photos")

if __name__ == "__main__":
    main()
