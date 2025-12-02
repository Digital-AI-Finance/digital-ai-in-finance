"""
Complete MSCA photo scraper - downloads ALL photos
"""

from playwright.sync_api import sync_playwright
import requests
import json
import time
import re
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

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
    print("Scraping ALL MSCA photos...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.digital-finance-msca.com/our-people', wait_until='networkidle')
        time.sleep(5)

        # Scroll extensively
        for i in range(40):
            page.evaluate(f'window.scrollTo(0, {i*350})')
            time.sleep(0.2)

        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(2)

        for i in range(50):
            page.evaluate(f'window.scrollTo(0, {i*300})')
            time.sleep(0.15)

        # Get all person entries by finding image+name pairs
        data = page.evaluate('''() => {
            const results = [];
            const seen = new Set();

            // Find all circular images (profile photos)
            document.querySelectorAll('img').forEach(img => {
                const src = img.src || img.dataset.src || '';
                if (!src.includes('wixstatic')) return;
                if (seen.has(src)) return;

                const style = window.getComputedStyle(img);
                const parent = img.closest('[data-testid]') || img.parentElement?.parentElement?.parentElement;

                // Look for name text near this image
                let name = '';
                let searchEl = img.parentElement;

                for (let i = 0; i < 8 && searchEl; i++) {
                    const walker = document.createTreeWalker(searchEl, NodeFilter.SHOW_TEXT);
                    let node;
                    while (node = walker.nextNode()) {
                        const txt = node.textContent.trim();
                        if (txt.length >= 5 && txt.length <= 45) {
                            const words = txt.split(/\\s+/);
                            if (words.length >= 2 && words.length <= 5) {
                                if (words.every(w => /^[A-Z]/.test(w))) {
                                    if (!/University|Institute|Center|School|European|Horizon|Research|Department|Grant|Funded/i.test(txt)) {
                                        name = txt;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    if (name) break;
                    searchEl = searchEl.parentElement;
                }

                if (name && !seen.has(name)) {
                    seen.add(src);
                    seen.add(name);
                    results.push({name, url: src});
                }
            });

            return results;
        }''')

        browser.close()

    print(f"Found {len(data)} people with photos")

    # Download all
    downloaded = {}
    for item in data:
        name = item['name']
        url = item['url']
        fn = sanitize(name)
        if not fn:
            continue

        ext = '.png' if '.png' in url else '.jpg'
        fpath = ASSETS_DIR / (fn + ext)

        # Check if exists and is good
        if fpath.exists() and fpath.stat().st_size > 5000:
            downloaded[name] = fn + ext
            continue

        size = download(url, fpath)
        if size > 0:
            downloaded[name] = fn + ext
            try:
                print(f"  {name}: {size/1024:.1f}KB")
            except:
                print(f"  [name]: {size/1024:.1f}KB")

    print(f"\nDownloaded: {len(downloaded)}")

    # Update mappings
    mappings = {'people': []}
    for name, fn in downloaded.items():
        mappings['people'].append({'name': name, 'filename': fn})

    # Add any existing photos not in downloaded
    for fpath in ASSETS_DIR.glob('*.*'):
        if fpath.suffix.lower() in ['.jpg', '.png'] and fpath.stat().st_size > 3000:
            name = ' '.join(w.title() for w in fpath.stem.replace('_', ' ').replace('-', ' ').split())
            if not any(p['filename'] == fpath.name for p in mappings['people']):
                mappings['people'].append({'name': name, 'filename': fpath.name})

    with open(DATA_DIR / 'msca_people_named.json', 'w') as f:
        json.dump(mappings, f, indent=2)

    print(f"Total mappings: {len(mappings['people'])}")

    # Check committee
    with open(DATA_DIR / 'scientific_committee.json') as f:
        committee = json.load(f)['selected']

    print(f"\nCommittee status:")
    found = 0
    for m in committee:
        fn = sanitize(m)
        has = any((ASSETS_DIR / (fn + e)).exists() and (ASSETS_DIR / (fn + e)).stat().st_size > 3000
                  for e in ['.jpg', '.png'])
        if has:
            found += 1
            print(f"  [OK] {m}")
        else:
            print(f"  [--] {m}")

    print(f"\nCommittee: {found}/{len(committee)}")

if __name__ == "__main__":
    main()
