"""
Scrape ALL real photos from MSCA Digital Finance website
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

def scrape_photos():
    print("Starting browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading MSCA page...")
        page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        time.sleep(3)

        # Scroll multiple times to load all content
        print("Scrolling to load all images...")
        for i in range(20):
            page.evaluate("window.scrollBy(0, 500)")
            time.sleep(0.3)

        # Scroll back and wait
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        # Scroll again slowly
        for i in range(25):
            page.evaluate("window.scrollBy(0, 400)")
            time.sleep(0.2)

        print("Extracting image data...")

        # Get all images with their nearby text
        data = page.evaluate('''() => {
            const results = [];
            const images = document.querySelectorAll('img');
            const seenUrls = new Set();

            images.forEach(img => {
                const src = img.src || img.dataset.src || '';
                if (!src || seenUrls.has(src)) return;
                if (!src.includes('wixstatic.com')) return;

                // Skip tiny images (icons, logos)
                const width = img.naturalWidth || img.width || 0;
                const height = img.naturalHeight || img.height || 0;
                if (width < 50 || height < 50) return;

                seenUrls.add(src);

                // Find nearby text that might be a name
                let name = '';
                let parent = img.parentElement;

                for (let i = 0; i < 5 && parent; i++) {
                    // Look for text elements nearby
                    const texts = parent.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6, div');
                    for (const t of texts) {
                        const txt = t.innerText.trim();
                        // Check if looks like a name (2-4 words, capitalized)
                        if (txt && txt.length > 4 && txt.length < 40) {
                            const words = txt.split(/\s+/);
                            if (words.length >= 2 && words.length <= 4) {
                                if (/^[A-Z]/.test(words[0]) && /^[A-Z]/.test(words[words.length-1])) {
                                    // Skip if it's an institution name
                                    if (!/University|Institute|Center|School|Department/i.test(txt)) {
                                        name = txt;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    if (name) break;
                    parent = parent.parentElement;
                }

                // Get high-res URL
                let highRes = src;
                // Convert to higher resolution
                highRes = highRes.replace(/\/w_\d+,h_\d+/, '/w_300,h_300');
                highRes = highRes.replace(/fill\/w_\d+,h_\d+/, 'fill/w_300,h_300');

                results.push({
                    url: highRes,
                    name: name,
                    origUrl: src
                });
            });

            return results;
        }''')

        browser.close()
        return data

def download_photo(url, filename):
    """Download photo if it's a real image (not placeholder)"""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            content = resp.content
            # Check if it's a real photo (placeholders are small)
            if len(content) > 3000:
                filepath = ASSETS_DIR / filename
                with open(filepath, 'wb') as f:
                    f.write(content)
                return True, len(content)
        return False, 0
    except Exception as e:
        return False, 0

def main():
    print("Scraping all photos from MSCA...")

    # Load committee members
    with open(DATA_DIR / "scientific_committee.json", 'r') as f:
        committee = json.load(f)['selected']

    committee_lower = {c.lower(): c for c in committee}

    # Scrape
    images = scrape_photos()
    print(f"Found {len(images)} images")

    # Track downloads
    downloaded = {}

    for img in images:
        name = img.get('name', '')
        url = img.get('url', '')

        if not name or not url:
            continue

        name_lower = name.lower()

        # Check if this is a committee member
        matched_member = None
        for cm_lower, cm in committee_lower.items():
            # Check various matching strategies
            if cm_lower == name_lower:
                matched_member = cm
                break
            # Check if names overlap significantly
            cm_parts = set(cm_lower.split())
            name_parts = set(name_lower.split())
            if len(cm_parts & name_parts) >= 2:
                matched_member = cm
                break

        if matched_member and matched_member not in downloaded:
            filename = sanitize_filename(matched_member)
            ext = '.png' if '.png' in url.lower() else '.jpg'
            full_filename = filename + ext

            success, size = download_photo(url, full_filename)
            if success:
                downloaded[matched_member] = {
                    'filename': full_filename,
                    'url': url,
                    'size': size
                }
                try:
                    print(f"  Downloaded: {matched_member} ({size/1024:.1f}KB)")
                except:
                    print(f"  Downloaded: [name] ({size/1024:.1f}KB)")

    print(f"\nDownloaded {len(downloaded)} / {len(committee)} committee member photos")

    # Also download any other images we found with names
    print("\nDownloading other named people...")
    other_count = 0
    for img in images:
        name = img.get('name', '')
        url = img.get('url', '')
        if not name or not url:
            continue
        if name in downloaded:
            continue

        filename = sanitize_filename(name)
        if not filename:
            continue
        ext = '.png' if '.png' in url.lower() else '.jpg'
        full_filename = filename + ext

        # Skip if already exists
        if (ASSETS_DIR / full_filename).exists():
            continue

        success, size = download_photo(url, full_filename)
        if success:
            other_count += 1

    print(f"Downloaded {other_count} additional photos")

    # Update the mappings file
    mappings = {'people': []}
    for member, info in downloaded.items():
        mappings['people'].append({
            'name': member,
            'filename': info['filename'],
            'url': info['url']
        })

    # Add existing mappings for people we already have
    existing = load_existing_mappings()
    for person in existing.get('people', []):
        if person['name'] not in downloaded:
            # Check if file exists and is real
            fpath = ASSETS_DIR / person['filename']
            if fpath.exists() and fpath.stat().st_size > 3000:
                mappings['people'].append(person)

    with open(DATA_DIR / "msca_people_named.json", 'w') as f:
        json.dump(mappings, f, indent=2)

    print(f"\nUpdated mappings: {len(mappings['people'])} people with real photos")

    # Report missing committee members
    missing = [c for c in committee if c not in downloaded and not has_existing_photo(c)]
    if missing:
        print(f"\nMissing photos for {len(missing)} committee members:")
        for m in missing:
            try:
                print(f"  - {m}")
            except:
                print("  - [name with special chars]")

def load_existing_mappings():
    fpath = DATA_DIR / "msca_people_named.json"
    if fpath.exists():
        with open(fpath, 'r') as f:
            return json.load(f)
    return {'people': []}

def has_existing_photo(name):
    """Check if we have a real photo for this person"""
    filename = sanitize_filename(name)
    for ext in ['.jpg', '.png']:
        fpath = ASSETS_DIR / (filename + ext)
        if fpath.exists() and fpath.stat().st_size > 3000:
            return True
    return False

if __name__ == "__main__":
    main()
