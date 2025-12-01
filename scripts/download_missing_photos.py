"""
Download photos for specific missing committee members
"""

from playwright.sync_api import sync_playwright
import requests
import time
import re
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"

MISSING = [
    'Codruta Mare',
    'Alexandra-Ioana Conda',
    'Daniel Traian Pele',
    'Ralf Korn',
    'Kristina Sutiene',
    'Stefan Theussl',
    'Albulena Shala',
    'Rezarta Perri'
]

def sanitize(name):
    name = re.sub(r'^(Prof\.|Dr\.|Mr\.|Ms\.)\s*', '', name)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    safe = re.sub(r'[^\w\s-]', '', name.lower())
    return re.sub(r'[\s]+', '_', safe.strip())

def download(url, filepath):
    try:
        url = re.sub(r'/w_\d+,h_\d+', '/w_400,h_400', url)
        url = re.sub(r'fill/w_\d+,h_\d+', 'fill/w_400,h_400', url)
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 2000:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            return len(resp.content)
    except:
        pass
    return 0

def main():
    print("Downloading missing committee photos...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.digital-finance-msca.com/our-people', wait_until='networkidle')
        time.sleep(5)

        # Scroll to load all
        for i in range(40):
            page.evaluate(f'window.scrollTo(0, {i*350})')
            time.sleep(0.2)

        for name in MISSING:
            print(f"\nSearching for: {name}")

            try:
                # Find the name element
                name_el = page.locator(f'text="{name}"').first
                name_el.scroll_into_view_if_needed()
                time.sleep(0.3)

                # Get position
                box = name_el.bounding_box()
                if not box:
                    print(f"  Could not find position")
                    continue

                # Find nearest image by evaluating JS
                img_url = page.evaluate(f'''(nameY) => {{
                    const images = document.querySelectorAll('img');
                    let closest = null;
                    let minDist = Infinity;

                    images.forEach(img => {{
                        const src = img.src || '';
                        if (!src.includes('wixstatic')) return;

                        const rect = img.getBoundingClientRect();
                        // Image should be above or at same level as name
                        const dist = Math.abs(rect.bottom - nameY) + Math.abs(rect.left - 100);

                        if (dist < minDist && rect.width > 50) {{
                            minDist = dist;
                            closest = src;
                        }}
                    }});

                    return closest;
                }}''', box['y'])

                if img_url:
                    print(f"  Found image: {img_url[:60]}...")

                    fn = sanitize(name)
                    ext = '.png' if '.png' in img_url else '.jpg'
                    fpath = ASSETS_DIR / (fn + ext)

                    size = download(img_url, fpath)
                    if size > 0:
                        print(f"  Downloaded: {size/1024:.1f} KB")
                    else:
                        print(f"  Download failed")
                else:
                    print(f"  No image found nearby")

            except Exception as e:
                print(f"  Error: {e}")

        browser.close()

    print("\nDone!")

if __name__ == "__main__":
    main()
